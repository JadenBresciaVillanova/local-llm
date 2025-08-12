#//backend/api/chat.py
import datetime
import os
import json
import time
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

# LangChain Imports
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.vectorstores.pgvector import PGVector
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_community.cross_encoders import HuggingFaceCrossEncoder
from langchain.retrievers.document_compressors import CrossEncoderReranker
from langchain.retrievers.contextual_compression import ContextualCompressionRetriever

# Local Imports
from backend.db.session import SYNC_DATABASE_URL
from backend.schemas.chat_schema import ChatRequest, ChatResponse, TokenCounts
from backend.api.auth_utils import get_current_user
from backend.models.user import User
from backend.db.mongodb import get_mongo_db
from backend.services.sandbox_service import SandboxService
from backend.services.metrics_service import MetricsService
from backend.services.kafka_logger import get_kafka_logger

# --- Environment Setup & Constants ---
router = APIRouter()
OLLAMA_BASE_URL = os.getenv("OLLAMA_HOST", "http://ollama:11434")
VALID_MODELS = [
    "llama3.1:8b", "codellama:7b", "gemma:7b", "dolphin-mistral:7b", 
    "deepseek-r1:7b", "gpt-oss:20b", "qwen3:8b"
]

# --- 1. PROMPT TEMPLATES ---

# Prompt 1: The Triage Agent - Classifies query complexity
TRIAGE_PROMPT_TEMPLATE = """
You are a master AI dispatcher. Your first task is to analyze the user's query and classify it into one of two categories: "Simple" or "Complex".

- A "Simple" query is a single, self-contained request that can be answered by one model WITHOUT needing to refer to external documents or previous conversation turns.
  - Examples: "What is Python?", "Write a short poem about space.", "Translate 'hello' to French."

- A "Complex" query involves one or more of the following:
  1.  **Requires using an attached document or file context.** (e.g., "Summarize the attached file," "Based on this document, what are the key risks?")
  2.  Involves multiple distinct steps or skills. (e.g., "Analyze this code for bugs AND write a report.")
  3.  Requires looking at the chat history to be understood. (e.g., "Explain that last point in more detail.")

You must respond with a JSON object containing two keys:
1. "complexity": Your classification, either "Simple" or "Complex".
2. "reasoning": A brief, one-sentence explanation for your choice.

User Query:
{question}

Triage Decision:
"""
triage_prompt = PromptTemplate.from_template(TRIAGE_PROMPT_TEMPLATE)


# Prompt 2: The Performance-Aware Router - Selects the best model for SIMPLE tasks
PERFORMANCE_ROUTER_PROMPT_TEMPLATE = """
You are an efficiency-focused AI dispatcher. Your goal is to choose the model with the best balance of quality, speed, and resource cost for the user's task.

Model Performance Profile:
[
  {{ "name": "llama3.1:8b", "quality": 8, "speed": 7, "resource_cost": 6, "strengths": "General, RAG, reliable" }},
  {{ "name": "codellama:7b", "quality": 9, "speed": 6, "resource_cost": 7, "strengths": "Complex code, algorithms" }},
  {{ "name": "gemma:7b", "quality": 8, "speed": 9, "resource_cost": 5, "strengths": "Fast, general, good at simple code" }},
  {{ "name": "dolphin-mistral:7b", "quality": 8, "speed": 8, "resource_cost": 6, "strengths": "Creative, less filtered code & text" }},
  {{ "name": "deepseek-r1:7b", "quality": 9, "speed": 7, "resource_cost": 6, "strengths": "Reasoning-focused, balanced performance" }},
  {{ "name": "gpt-oss:20b", "quality": 10, "speed": 5, "resource_cost": 9, "strengths": "Very high quality, complex reasoning & generation" }},
  {{ "name": "qwen3:8b", "quality": 9, "speed": 6, "resource_cost": 7, "strengths": "Hybrid reasoning, multilingual, long context support" }}
]

Analyze the User Query below. Based on your analysis and the model profiles, your response MUST be ONLY the "name" value of the single best model. Do not include any other words, backticks, or explanation.

User Query:
{question}

Chosen Model Name:
"""
performance_router_prompt = PromptTemplate.from_template(PERFORMANCE_ROUTER_PROMPT_TEMPLATE)

# Prompt 3: The Stateful Multi-Model Agent (V6)
TOOL_USER_PROMPT_TEMPLATE = """
You are a methodical and precise project manager AI. Your single most important goal is to fulfill the user's request accurately and efficiently, and then stop. **You must not perform extra, unrequested work.**

**Your Workflow:**

1.  **Deconstruct the Goal:** First, read the user's request and break it down into a mental checklist of all the distinct things they have asked for.

2.  **Check Progress Against the Goal:** Next, review the 'Conversation History'. For each item on your mental checklist, check if there is already an 'Observation' that satisfies it.

3.  **Execute the NEXT Unfinished Task:**
    -   **If there are unfinished items on your checklist**, identify the single most important one to do next.
    -   Select the best model from the 'Model Performance Profile' to accomplish that specific task.
    -   Use the `call_model` tool to execute it. Your 'task' description must be precise and self-contained. 
    -   **CRITICAL**: If document context is available and relevant to the task, explicitly instruct the model to use it by starting your task with "Based on the document context provided, [do X]" or "Using only information from the provided documents, [do X]".

4.  **Provide the Final Answer:**
    -   **If, and only if, every single item on your mental checklist has been satisfied** by an 'Observation' in the history, your job is complete.
    -   Use the `final_answer` tool. Your response should synthesize the 'Observations' to directly answer the user's original request. **Do not add any new analysis in the final answer.**

---
**Model Performance Profile (Your Available Tools):**
[
  {{
    "name": "llama3.1:8b",
    "strengths": "Excellent for general reasoning, summarization, understanding documents, and planning. Your 'thinking' brain."
  }},
  {{
    "name": "codellama:7b",
    "strengths": "Specialist for writing, debugging, and explaining complex code, especially Python and algorithms."
  }},
  {{
    "name": "gemma:7b",
    "strengths": "Very fast for simple, general tasks like basic text generation, reformatting, or simple code snippets."
  }},
  {{
    "name": "dolphin-mistral:7b",
    "strengths": "Best for creative tasks, writing in a specific style, or generating less-filtered/more 'human-like' text and code."
  }},
  {{
    "name": "deepseek-r1:7b",
    "strengths": "Strong reasoning and logic capabilities, a good balance between code and text understanding."
  }},
  {{
    "name": "gpt-oss:20b",
    "strengths": "The most powerful model. Use for highly complex reasoning, multi-faceted analysis, or when the highest quality output is required, despite being slower."
  }}, 
  {{
    "name": "qwen3:8b",
    "strengths": "Excellent for tasks involving multiple languages, long documents, or a hybrid of complex reasoning and generation."
  }}
]

---
**Tool Formats:**
1.  **Execute a step:** `{{"tool_to_use": "call_model", "model": "model_name", "task": "The specific task to perform."}}`
2.  **Finish the job:** `{{"final_answer": "The complete, synthesized answer."}}`

---
**User Request:**
{question}

**Document Context:**
{document_context}

**Conversation History (Your previous thoughts and the results):**
{history}

**YOUR NEXT ACTION (A single JSON object based on the workflow above):**
"""
tool_user_prompt = PromptTemplate.from_template(TOOL_USER_PROMPT_TEMPLATE)


# Other General Prompts
REWRITE_PROMPT_TEMPLATE = "Based on the chat history, reformulate the question to be a standalone question. Chat History: {chat_history}\n\nQuestion: {question}\n\nStandalone Question:"
rewrite_prompt = PromptTemplate.from_template(REWRITE_PROMPT_TEMPLATE)

DEFAULT_RAG_PROMPT_TEMPLATE = "Use ONLY the following context to answer the question. If you don't know, say you don't know.\n\nCONTEXT:\n{context}\n\nQUESTION:\n{question}\n\nANSWER:"
default_rag_prompt = PromptTemplate.from_template(DEFAULT_RAG_PROMPT_TEMPLATE)

CODE_PROMPT_TEMPLATE = "You are an expert programmer. Provide a correct code solution. Use the context if relevant.\n\nCONTEXT:\n{context}\n\nREQUEST:\n{question}\n\nCODE:"
code_prompt = PromptTemplate.from_template(CODE_PROMPT_TEMPLATE)

PROMPT_FOR_MODEL = { "codellama:7b": code_prompt, "gemma:7b": code_prompt, "dolphin-mistral:7b": code_prompt, "gpt-oss:20b": code_prompt,  "deepseek-r1:7b": code_prompt}

# --- Initialize Static Models ---
print("Initializing static models (embeddings, re-ranker)...")
embeddings = OllamaEmbeddings(model="nomic-embed-text", base_url=OLLAMA_BASE_URL)
cross_encoder_model = HuggingFaceCrossEncoder(model_name="cross-encoder/ms-marco-MiniLM-L-6-v2")
output_parser = StrOutputParser()
print("Static models initialized successfully.")


# --- WORKFLOW C: MULTI-MODEL AGENT (FOR COMPLEX TASKS) ---   
async def run_multi_agent_workflow(request: ChatRequest, current_user: User, mongo_db: AsyncIOMotorClient) -> ChatResponse:
    print("🚀 Entering Goal-Oriented Agent Workflow...")
    
    # --- STEP 1: CORRECTED CONTEXT RETRIEVAL ---
    document_context_str = ""
    if request.selected_file_ids:
        print(f"📄 User selected {len(request.selected_file_ids)} file(s): {request.selected_file_ids}. Retrieving content...")
        
        # Initialize the vector store
        vectorstore = PGVector(
            connection_string=SYNC_DATABASE_URL, 
            embedding_function=embeddings
        )

        # Build a filter to ONLY get chunks from the selected file_ids for the current user.
        # This is the most important part.
        file_id_strings = [str(fid) for fid in request.selected_file_ids]
        strict_filter = {
            "user_id": str(current_user.id),
            "file_id": {"$in": file_id_strings}
        }
        print(f"🔍 Debug: Filter - user_id: {str(current_user.id)}, file_ids: {file_id_strings}")

        # Create a retriever that is BOUND by this strict filter.
        # We set 'k' to a high number to ensure we get all chunks from the selected file(s),
        # as the filter is what truly limits the search space.
        base_retriever = vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 100, "filter": strict_filter} 
        )

        # The reranker will then re-order the chunks from ONLY the selected files
        # and pick the top N most relevant to the query.
        reranker = CrossEncoderReranker(model=cross_encoder_model, top_n=5)
        compression_retriever = ContextualCompressionRetriever(
            base_compressor=reranker, 
            base_retriever=base_retriever
        )
        
        # Try semantic search first
        final_context_docs = await compression_retriever.ainvoke(request.prompt)
        
        # If semantic search fails, try to get ALL chunks from the selected files
        if not final_context_docs:
            print("Semantic search found no relevant chunks. Trying to retrieve ALL chunks from selected files...")
            try:
                # Use a very broad search query to get all chunks
                fallback_docs = await base_retriever.ainvoke("document content text")
                if fallback_docs:
                    # Limit to prevent overwhelming the context
                    final_context_docs = fallback_docs[:10] 
                    print(f"Fallback: Retrieved {len(final_context_docs)} chunks from selected file(s).")
                else:
                    # Last resort: try without any query filter
                    print("Trying without query filtering...")
                    vectorstore_simple = PGVector(
                        connection_string=SYNC_DATABASE_URL, 
                        embedding_function=embeddings
                    )
                    simple_retriever = vectorstore_simple.as_retriever(
                        search_type="similarity",
                        search_kwargs={"k": 20, "filter": strict_filter}
                    )
                    final_context_docs = await simple_retriever.ainvoke("text")
                    if final_context_docs:
                        print(f"Simple retrieval: Got {len(final_context_docs)} chunks.")
            except Exception as e:
                print(f"Error in fallback retrieval: {e}")
        
        if final_context_docs:
            document_context_str = "\n".join([doc.page_content for doc in final_context_docs])
            print(f"Final: Using {len(final_context_docs)} document chunks for context.")
        else:
            print("Could not retrieve any document content from selected files.")

    else:
        print("No files selected by user. Agent will proceed without document context.")

    # Step 2: Initialize the Planner/Agent using the V7 Context-Aware Prompt
    planner_llm = ChatOllama(model="llama3.1:8b", temperature=0, format="json", base_url=OLLAMA_BASE_URL)
    planner_chain = tool_user_prompt | planner_llm | StrOutputParser()

    # Step 3: Begin the agent execution loop
    agent_history: List[str] = []
    response_text = ""
    MAX_STEPS = 2
    step_count = 0

    while step_count < MAX_STEPS:
        step_count += 1
        print(f"\n--- Agent Step {step_count}/{MAX_STEPS} ---")
        
        history_str = "\n".join(agent_history)
        
        # Pass context explicitly to the planner via the new {document_context} variable
        llm_decision_str = await planner_chain.ainvoke({
            "question": request.prompt, 
            "document_context": document_context_str if document_context_str else "No document context provided.",
            "history": history_str
        })
        print(f"Planner's Raw JSON Decision:\n{llm_decision_str}")
        agent_history.append(f"Step {step_count} Thought:\n{llm_decision_str}")
        
        try:
            decision_json = json.loads(llm_decision_str)
            
            if decision_json.get("tool_to_use") == "call_model":
                print("Agent requested to call a model tool.")
                model_to_call = decision_json.get("model")
                task_for_model = decision_json.get("task")

                if not model_to_call or not task_for_model:
                    observation = "Observation: Invalid tool call. Missing 'model' or 'task'."
                    print(f"  {observation}")
                    agent_history.append(observation)
                    # Don't continue here - count this as a step and move forward
                else:
                    print(f"   - Model Selected: '{model_to_call}', Task: '{task_for_model}'")
                    print(f"   - Document context available: {bool(document_context_str)}")
                    if document_context_str:
                        print(f"   - Context length: {len(document_context_str)} chars")
                    
                    # Validate model name
                    if model_to_call not in VALID_MODELS:
                        print(f"  Invalid model '{model_to_call}'. Using llama3.1:8b instead.")
                        model_to_call = "llama3.1:8b"
                    
                    print(f"   - Final model to use: '{model_to_call}'")
                    
                    worker_llm = ChatOllama(model=model_to_call, temperature=0, base_url=OLLAMA_BASE_URL)
                    
                    # Enhanced prompt to ensure the worker model uses document context effectively
                    if document_context_str:
                        worker_prompt = PromptTemplate.from_template(
                            "You are a specialist model. Your job is to perform a single specific task using the provided document context.\n\n"
                            "IMPORTANT: Read the entire document context below and answer based ONLY on what you see in the document. Be direct and specific.\n\n"
                            "DOCUMENT CONTEXT:\n{context}\n\n"
                            "YOUR SPECIFIC TASK:\n{task}\n\n"
                            "RESPONSE (be direct and concise):"
                        )
                    else:
                        worker_prompt = PromptTemplate.from_template(
                            "You are a specialist model. Your job is to perform a single specific task.\n\n"
                            "YOUR SPECIFIC TASK:\n{task}\n\n"
                            "RESPONSE:"
                        )
                    
                    worker_chain = worker_prompt | worker_llm | StrOutputParser()
                    
                    if document_context_str:
                        tool_result = await worker_chain.ainvoke({
                            "context": document_context_str, 
                            "task": task_for_model
                        })
                    else:
                        tool_result = await worker_chain.ainvoke({
                            "task": task_for_model
                        })

                    print(f"   -  Tool Result: '{tool_result[:200]}...'")
                    observation = f"Observation from calling model '{model_to_call}':\n{tool_result}"
                    agent_history.append(observation)

            elif "final_answer" in decision_json:
                print("🏁 Agent decided to give the Final Answer.")
                response_text = decision_json["final_answer"]
                break
            
            else:
                observation = "Observation: Your response was not a recognized tool. Use 'call_model' or 'final_answer'."
                print(f" {observation}")
                agent_history.append(observation)

        except (json.JSONDecodeError, KeyError) as e:
            observation = f"Observation: Your last response was not valid JSON. Error: {str(e)}. You must respond with a single JSON object."
            print(f" {observation} | Raw response was: {llm_decision_str}")
            agent_history.append(observation)

    # If we exit the loop without a final answer
    if not response_text:
        print("⚠️ Agent reached max steps without providing a final answer.")
        last_observation = next((line for line in reversed(agent_history) if line.startswith("Observation")), "The agent could not complete the request.")
        response_text = f"The agent reached its maximum number of steps ({MAX_STEPS}).\n\nLast known information:\n{last_observation}"

    # --- Save final result to MongoDB ---
    convo_id_obj = ObjectId(request.conversation_id) if request.conversation_id else ObjectId()
    new_messages = [{"role": "user", "message": request.prompt}, {"role": "ai", "message": response_text}]
    await mongo_db.conversations.update_one(
        {"_id": convo_id_obj, "user_id": str(current_user.id)},
        {"$push": {"messages": {"$each": new_messages}}, "$setOnInsert": {"user_id": str(current_user.id), "created_at": datetime.datetime.now(datetime.timezone.utc)}},
        upsert=True
    )
    return ChatResponse(response=response_text, conversation_id=str(convo_id_obj), token_counts=None)


# --- WORKFLOW B: PERFORMANCE-AWARE ROUTER (FOR SIMPLE TASKS) ---
async def run_performance_aware_router(request: ChatRequest, current_user: User, mongo_db: AsyncIOMotorClient) -> ChatResponse:
    print(" Query is simple. Engaging Performance-Aware Router...")
    router_llm = ChatOllama(model="llama3.1:8b", temperature=0, base_url=OLLAMA_BASE_URL)
    model_selection_chain = performance_router_prompt | router_llm | StrOutputParser()
    chosen_model_str = await model_selection_chain.ainvoke({"question": request.prompt})
    
    # --- ROBUST PARSING BLOCK ---
    model_to_use = None
    for model in VALID_MODELS:
        if model in chosen_model_str.lower():
            model_to_use = model
            break

    if not model_to_use:
        print(f" Performance router returned an invalid model name: '{chosen_model_str}'. Defaulting to 'llama3.1:8b'.")
        model_to_use = "llama3.1:8b"
    
    print(f" Performance router has chosen model: '{model_to_use}'")
    return await run_rag_pipeline(request, current_user, mongo_db, model_name=model_to_use)


# --- WORKFLOW A: THE CORE RAG PIPELINE (THE ENGINE) ---
async def run_rag_pipeline(request: ChatRequest, current_user: User, mongo_db: AsyncIOMotorClient, model_name: str) -> ChatResponse:
    print(f"--- Running RAG Pipeline with model: '{model_name}' ---")

    llm = ChatOllama(model=model_name, temperature=request.temperature, top_p=request.top_p, num_predict=request.max_tokens, base_url=OLLAMA_BASE_URL)
    
    chat_history_str = ""
    rewritten_query = request.prompt
    if request.conversation_id:
        convo = await mongo_db.conversations.find_one({"_id": ObjectId(request.conversation_id), "user_id": str(current_user.id)})
        if convo and convo.get("messages"):
            messages = [f"{msg['role']}: {msg['message']}" for msg in convo["messages"]]
            chat_history_str = "\n".join(messages)
            
            # Rewrite query based on history
            rewriter_chain = rewrite_prompt | llm | StrOutputParser()
            rewritten_query = await rewriter_chain.ainvoke({"chat_history": chat_history_str, "question": request.prompt})
            print(f"Rewritten query for retrieval: '{rewritten_query}'")

    final_context_docs = []
    if request.selected_file_ids:
        print(f"📄 Retrieving context for RAG...")
        vectorstore = PGVector(connection_string=SYNC_DATABASE_URL, embedding_function=embeddings)
        base_retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 20, "filter": {"user_id": str(current_user.id), "file_id": {"$in": [str(fid) for fid in request.selected_file_ids]}}})
        reranker = CrossEncoderReranker(model=cross_encoder_model, top_n=5)
        compression_retriever = ContextualCompressionRetriever(base_compressor=reranker, base_retriever=base_retriever)
        final_context_docs = await compression_retriever.ainvoke(rewritten_query)
        print(f"Retrieved {len(final_context_docs)} final documents for context.")

    final_rag_prompt = PROMPT_FOR_MODEL.get(model_name, default_rag_prompt)
    if request.custom_prompt_template:
        try: 
            final_rag_prompt = PromptTemplate.from_template(request.custom_prompt_template)
            print(" Using custom prompt template from user.")
        except Exception as e:
            print(f"⚠️ Warning: Invalid custom prompt template. Using default. Error: {e}")
    else:
        print(f" Using specialized prompt for model '{model_name}' or default.")

    context_str = "\n\n---\n\n".join([doc.page_content for doc in final_context_docs]) if final_context_docs else "No context available."
    
    rag_chain = final_rag_prompt | llm
    llm_response = await rag_chain.ainvoke({"context": context_str, "question": rewritten_query})
    
    response_text = llm_response.content
    response_metadata = llm_response.response_metadata
    prompt_tokens = response_metadata.get("prompt_eval_count", 0)
    response_tokens = response_metadata.get("eval_count", 0)
    token_counts = TokenCounts(prompt_tokens=prompt_tokens, response_tokens=response_tokens, total_tokens=prompt_tokens + response_tokens)
    
    convo_id_obj = ObjectId(request.conversation_id) if request.conversation_id else ObjectId()
    new_messages = [{"role": "user", "message": request.prompt}, {"role": "ai", "message": response_text}]
    await mongo_db.conversations.update_one(
        {"_id": convo_id_obj, "user_id": str(current_user.id)},
        {"$push": {"messages": {"$each": new_messages}}, "$setOnInsert": {"user_id": str(current_user.id), "created_at": datetime.datetime.now(datetime.timezone.utc)}},
        upsert=True
    )
    print(f" Successfully saved to conversation. ID: {convo_id_obj}")
    return ChatResponse(response=response_text, conversation_id=str(convo_id_obj), token_counts=token_counts)


# --- MAIN CHAT HANDLER (THE TRIAGE ROUTER) ---
@router.post("/chat", response_model=ChatResponse)
async def handle_chat_request(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    mongo_db: AsyncIOMotorClient = Depends(get_mongo_db),
):
    start_time = time.time()
    kafka_logger = get_kafka_logger()
    
    print(f"\n--- New Chat Request for user: {current_user.email} ---")
    print(f"Original question: '{request.prompt}'")
    
    try:
        # Log event
        kafka_logger.log_chat_message_sent(user_id=current_user.email, message=request.prompt, conversation_id=request.conversation_id or "new", model_name=request.selected_model)
        
        # --- PATH 1: USER OVERRIDE ---
        if request.selected_model != "agent-mode":
            print(f" User selected specific model: '{request.selected_model}'. Bypassing agent.")
            response = await run_rag_pipeline(request, current_user, mongo_db, model_name=request.selected_model)
        
        # --- PATH 2: AGENT MODE ---
        else:
            print(" Entering Agent Mode: Triage...")
            
            # Enhanced triage input to include file context information
            triage_input = request.prompt
            if request.selected_file_ids:
                triage_input += f"\n\n[Note: User has selected {len(request.selected_file_ids)} file(s) for context]"
            
            triage_llm = ChatOllama(model="llama3.1:8b", temperature=0, format="json", base_url=OLLAMA_BASE_URL)
            triage_chain = triage_prompt | triage_llm | StrOutputParser()
            
            triage_response_str = await triage_chain.ainvoke({"question": triage_input})
            
            complexity = "Simple" # Default to simple if JSON parsing fails
            try:
                triage_json = json.loads(triage_response_str)
                complexity = triage_json.get("complexity", "Simple")
                print(f" Triage decision: '{complexity}'. Reason: {triage_json.get('reasoning')}")
            except json.JSONDecodeError:
                print(f" Warning: Triage agent did not return valid JSON. Defaulting to Simple. Response: {triage_response_str}")
            
            # Force complex routing when files are selected for better document handling
            if request.selected_file_ids and complexity == "Simple":
                print(" Overriding to Complex due to selected files for better document handling")
                complexity = "Complex"

            # Route to the appropriate workflow based on complexity
            if complexity == "Complex":
                response = await run_multi_agent_workflow(request, current_user, mongo_db)
            else: 
                response = await run_performance_aware_router(request, current_user, mongo_db)
        
        # --- METRICS AND LOGGING ---
        end_time = time.time()
        response_time_ms = int((end_time - start_time) * 1000)
        
        MetricsService.record_chat_request(current_user.email, "success")
        MetricsService.record_llm_response_time(model_name=request.selected_model or "agent-mode", user_email=current_user.email, duration=end_time - start_time)
        kafka_logger.log_chat_message_received(user_id=current_user.email, response_length=len(response.response), conversation_id=request.conversation_id or "new", model_name=request.selected_model or "agent-mode", response_time_ms=response_time_ms)
        
        return response
        
    except Exception as e:
        print(f"❌❌❌ An unhandled error occurred: {e}")
        # Record failure metrics
        MetricsService.record_chat_request(current_user.email, "failure")
        MetricsService.record_chat_failure(current_user.email, type(e).__name__)
        
        # Log error event
        kafka_logger.log_error_occurred(user_id=current_user.email, error_type=type(e).__name__, error_message=str(e), endpoint="/api/chat")
        
        # Re-raise the exception to be handled by FastAPI's error handling
        raise HTTPException(status_code=500, detail=str(e)) from e