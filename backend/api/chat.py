# # backend/api/chat.py
# import json
# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.ext.asyncio import AsyncSession
# from motor.motor_asyncio import AsyncIOMotorClient
# from bson import ObjectId

# from backend.db.session import get_db
# from backend.db.mongodb import get_mongo_db
# from backend.services.ollama_client import OllamaClient
# from backend.schemas.chat_schema import ChatRequest, ChatResponse
# # This is a placeholder for a real auth dependency
# from .utils import get_current_user 
# from backend.models.user import User

# router = APIRouter()

# # ADD THIS TEST ROUTE
# @router.get("/health")
# def health_check():
#     return {"status": "ok", "router": "chat"}

# @router.post("/chat", response_model=ChatResponse)
# async def handle_chat_request(
#     request: ChatRequest,
#     db: AsyncSession = Depends(get_db),
#     mongo_db: AsyncIOMotorClient = Depends(get_mongo_db),
#     # In a real app, you'd get the user ID from a validated JWT token
#     current_user: User = Depends(get_current_user)
# ):
#     print(f"Received chat request from user ID: {current_user.id} ({current_user.email})")
#     ollama_client = OllamaClient(model="llama3:8b") # Or get model from config
    
#     # --- 1. Get AI response ---
#     ai_response_text = await ollama_client.generate(prompt=request.prompt)

#     if "Error:" in ai_response_text:
#         raise HTTPException(status_code=500, detail=ai_response_text)
        
#     # --- 2. Log conversation to MongoDB ---
#     conversations = mongo_db.conversations
    
#     new_message_exchange = [
#         {"role": "user", "message": request.prompt},
#         {"role": "ai", "message": ai_response_text}
#     ]
    
#     if request.conversation_id:
#         # Append to existing conversation
#         conv_id = ObjectId(request.conversation_id)
#         await conversations.update_one(
#             {"_id": conv_id, "user_id": str(current_user.id)},
#             {"$push": {"messages": {"$each": new_message_exchange}}}
#         )
#         conversation_id = request.conversation_id
#     else:
#         # Create a new conversation
#         result = await conversations.insert_one({
#             "user_id": str(current_user.id),
#             "messages": new_message_exchange
#         })
#         conversation_id = str(result.inserted_id)

#     # --- 3. (Optional) Simple logging to PostgreSQL ---
#     # from backend.models.chat_log import ChatLog
#     # new_log = ChatLog(
#     #     user_id=current_user.id,
#     #     prompt=request.prompt,
#     #     response=ai_response_text,
#     #     model_version_used=ollama_client.model
#     # )
#     # db.add(new_log)
#     # await db.commit()

#     return ChatResponse(response=ai_response_text, conversation_id=conversation_id)

# from fastapi import APIRouter
# from backend.schemas.chat_schema import ChatResponse # Keep schemas, they are simple Pydantic models

# router = APIRouter()

# @router.get("/chat/health")
# def health_check():
#     """A simple check to see if this router is being loaded."""
#     return {"status": "ok", "router": "chat"}

# @router.post("/chat", response_model=ChatResponse)
# async def handle_chat_request_simple():
#     """A simple, unauthenticated version of the chat endpoint."""
#     print("Simple chat endpoint was called!")
#     return ChatResponse(
#         response="This is a simple response from the un-authenticated endpoint.",
#         conversation_id="test-123"
#     )

# from fastapi import APIRouter
# from backend.schemas.chat_schema import ChatRequest, ChatResponse
# from backend.services.ollama_client import OllamaClient # <-- ADD THIS

# router = APIRouter()
# ollama_client = OllamaClient(model="llama3:8b") # <-- ADD THIS

# # Keep the health check for testing
# @router.get("/chat/health")
# def health_check():
#     return {"status": "ok", "router": "chat"}

# @router.post("/chat", response_model=ChatResponse)
# async def handle_chat_request(request: ChatRequest): # <-- Add the request body back
#     print(f"Ollama chat endpoint was called with prompt: {request.prompt}")
    
#     response_text = await ollama_client.generate(prompt=request.prompt)

#     return ChatResponse(
#         response=response_text,
#         conversation_id="test-123"
#     )
#end

# from fastapi import APIRouter, Depends, HTTPException
# from backend.db.mongodb import get_mongo_db
# from backend.schemas.chat_schema import ChatRequest, ChatResponse
# from backend.services.ollama_client import OllamaClient
# from backend.api.auth_utils import get_current_user # <-- Add this import
# from backend.models.user import User # <-- Add this import

# router = APIRouter()
# ollama_client = OllamaClient(model="llama3:8b")

# @router.post("/chat", response_model=ChatResponse)
# async def handle_chat_request_auth(
#     request: ChatRequest,
#     current_user: User = Depends(get_current_user) # <-- Add this dependency
    
# ):
#     print("✅ STEP 1 & 3: Authenticated endpoint was called successfully.")
#     print(f"--- User identified: {current_user.email} (ID: {current_user.id})")
    
#     try:
#         response_text = await ollama_client.generate(prompt=request.prompt)
#         print("✅ STEP 2: Ollama client returned a response successfully.")
#         return ChatResponse(
#             response=response_text,
#             conversation_id="test-auth"
#         )
#     except Exception as e:
#         print(f"❌ STEP 2 FAILED: Error calling Ollama. Details: {e}")
#         raise HTTPException(status_code=500, detail=f"Ollama Error: {e}")

# backend/api/chat.py
# import datetime
# from fastapi import APIRouter, Depends, HTTPException
# from motor.motor_asyncio import AsyncIOMotorClient
# from bson import ObjectId

# from backend.schemas.chat_schema import ChatRequest, ChatResponse
# from backend.services.ollama_client import OllamaClient
# from backend.api.auth_utils import get_current_user
# from backend.models.user import User
# from backend.db.mongodb import get_mongo_db

# router = APIRouter()
# ollama_client = OllamaClient(model="llama3:8b")

# @router.post("/chat", response_model=ChatResponse)
# async def handle_chat_request(
#     request: ChatRequest,
#     current_user: User = Depends(get_current_user),
#     mongo_db: AsyncIOMotorClient = Depends(get_mongo_db)
# ):
#     # ... (Ollama call remains the same) ...
#     response_text = await ollama_client.generate(prompt=request.prompt)

#     # --- THIS IS THE LOGIC YOU CAN NOW ADD BACK IN ---
#     try:
#         conversations = mongo_db.conversations
#         new_message_exchange = [{"role": "user", "message": request.prompt}, {"role": "ai", "message": response_text}]
#         conversation_id_str = request.conversation_id

#         if conversation_id_str:
#             conv_id = ObjectId(conversation_id_str)
#             await conversations.update_one({"_id": conv_id, "user_id": str(current_user.id)}, {"$push": {"messages": {"$each": new_message_exchange}}})
#         else:
#             new_convo_doc = {"user_id": str(current_user.id), "messages": new_message_exchange, "created_at": datetime.datetime.now(datetime.timezone.utc)}
#             result = await conversations.insert_one(new_convo_doc)
#             conversation_id_str = str(result.inserted_id)
        
#         print(f"✅ Successfully saved conversation to MongoDB. ID: {conversation_id_str}")

#     except Exception as e:
#         print(f"❌ Error saving to MongoDB: {e}")
#         return ChatResponse(response=response_text, conversation_id="") # Return empty convo_id on save failure

#     return ChatResponse(response=response_text, conversation_id=conversation_id_str)

# backend/api/chat.py
# import datetime
# from fastapi import APIRouter, Depends, HTTPException
# from motor.motor_asyncio import AsyncIOMotorClient
# from bson import ObjectId

# from backend.schemas.chat_schema import ChatRequest, ChatResponse
# from backend.services.ollama_client import OllamaClient
# from backend.api.auth_utils import get_current_user
# from backend.models.user import User
# from backend.db.mongodb import get_mongo_db

# router = APIRouter()
# ollama_client = OllamaClient(model="llama3:8b")

# def format_prompt_with_history(prompt: str, history: list) -> str:
#     """Formats a new prompt including the history of the conversation."""
#     formatted_history = "\n".join(
#         [f"{msg['role']}: {msg['message']}" for msg in history]
#     )
#     # This is a very simple context-injection strategy.
#     # You can get much more sophisticated with this.
#     return f"This is the conversation history:\n{formatted_history}\n\nNow, answer this new question: {prompt}"

# @router.post("/chat", response_model=ChatResponse)
# async def handle_chat_request(
#     request: ChatRequest,
#     current_user: User = Depends(get_current_user),
#     mongo_db: AsyncIOMotorClient = Depends(get_mongo_db)
# ):
#     conversations = mongo_db.conversations
#     conversation_id_str = request.conversation_id
    
#     final_prompt = request.prompt
    
#     # 1. If there's a conversation ID, fetch history and create a new prompt
#     if conversation_id_str:
#         conv_id = ObjectId(conversation_id_str)
#         conversation = await conversations.find_one(
#             {"_id": conv_id, "user_id": str(current_user.id)}
#         )
#         if conversation and "messages" in conversation:
#             print(f"Found conversation history with {len(conversation['messages'])} messages.")
#             final_prompt = format_prompt_with_history(request.prompt, conversation["messages"])

#     # 2. Get AI response using the (potentially modified) prompt
#     print(f"Sending final prompt to Ollama:\n--- START ---\n{final_prompt}\n--- END ---")
#     response_text = await ollama_client.generate(prompt=final_prompt)

#     # 3. Save the new exchange to MongoDB
#     new_message_exchange = [{"role": "user", "message": request.prompt}, {"role": "ai", "message": response_text}]
    
#     if conversation_id_str:
#         await conversations.update_one(
#             {"_id": conv_id},
#             {"$push": {"messages": {"$each": new_message_exchange}}}
#         )
#     else:
#         new_convo_doc = {"user_id": str(current_user.id), "messages": new_message_exchange, "created_at": datetime.datetime.now(datetime.timezone.utc)}
#         result = await conversations.insert_one(new_convo_doc)
#         conversation_id_str = str(result.inserted_id)
        
#     print(f"Successfully saved/updated conversation. ID: {conversation_id_str}")
#     return ChatResponse(response=response_text, conversation_id=conversation_id_str)

# backend/api/chat.py
# import datetime
# from fastapi import APIRouter, Depends, HTTPException
# from motor.motor_asyncio import AsyncIOMotorClient
# from bson import ObjectId
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.future import select

# # New imports for RAG
# from backend.models.embedding import DocumentChunk
# from backend.db.session import get_db

# from backend.schemas.chat_schema import ChatRequest, ChatResponse
# from backend.services.ollama_client import OllamaClient
# from backend.api.auth_utils import get_current_user
# from backend.models.user import User
# from backend.db.mongodb import get_mongo_db

# router = APIRouter()
# # We need an ollama client instance accessible to the whole file
# ollama_client = OllamaClient() 

# # --- New RAG-specific prompt template ---
# def format_prompt_with_rag_context(prompt: str, context: str) -> str:
#     """
#     Formats a prompt to include retrieved context for the RAG model.
#     """
#     return (
#         "You are an expert assistant. Use the following pieces of retrieved context to answer the user's question. "
#         "If you don't know the answer, just say that you don't know, don't try to make up an answer.\n\n"
#         "--- CONTEXT ---\n"
#         f"{context}\n"
#         "--- END CONTEXT ---\n\n"
#         f"Question: {prompt}"
#     )

# # ... (format_prompt_with_history can remain the same if you want to support non-RAG chat) ...

# async def retrieve_context_from_db(
#     db: AsyncSession, 
#     user_question: str, 
#     user: User,
#     # This could be passed in to filter by a specific file
#     # file_id: str | None = None, 
#     top_k: int = 5
# ) -> str:
#     """
#     1. Generates an embedding for the user's question.
#     2. Performs a similarity search in the DB for the most relevant chunks.
#     3. Returns the concatenated text of the top_k chunks.
#     """
#     # 1. Generate embedding for the user's question
#     question_embedding = await ollama_client.get_embedding(user_question)
#     if not question_embedding:
#         print("⚠️ Could not generate embedding for the question.")
#         return ""

#     # 2. Perform similarity search
#     # The l2_distance operator (<->) in pgvector finds the closest vectors.
#     # We are searching for chunks belonging to the current user.
#     stmt = (
#         select(DocumentChunk)
#         .join(DocumentChunk.file) # Join to filter by user
#         .where(User.id == user.id)
#         # In the future, you could add: .where(FileMetadata.id == file_id)
#         .order_by(DocumentChunk.embedding.l2_distance(question_embedding))
#         .limit(top_k)
#     )
    
#     result = await db.execute(stmt)
#     similar_chunks = result.scalars().all()
    
#     if not similar_chunks:
#         print("📚 No relevant document chunks found in the database.")
#         return ""

#     # 3. Concatenate the text of the top chunks
#     context = "\n\n---\n\n".join([chunk.text_content for chunk in similar_chunks])
#     print(f"📚 Retrieved {len(similar_chunks)} chunks to use as context.")
#     return context

# @router.post("/chat", response_model=ChatResponse)
# async def handle_chat_request(
#     request: ChatRequest,
#     current_user: User = Depends(get_current_user),
#     mongo_db: AsyncIOMotorClient = Depends(get_mongo_db),
#     sql_db: AsyncSession = Depends(get_db)
# ):
#     """
#     Handles a chat request. If it's a new conversation, it performs RAG.
#     If it's a continued conversation, it uses MongoDB history.
#     """
#     final_prompt = request.prompt
    
#     # Check if this is the start of a new conversation where we should use RAG
#     if not request.conversation_id:
#         # This is a new chat, let's assume it's a question for our documents
#         print("💬 New conversation. Performing RAG to find context...")
#         retrieved_context = await retrieve_context_from_db(
#             db=sql_db, 
#             user_question=request.prompt, 
#             user=current_user
#         )
        
#         if retrieved_context:
#             final_prompt = format_prompt_with_rag_context(request.prompt, retrieved_context)
#         else:
#             # If no context is found, just treat it as a normal question
#             print("No context found. Proceeding with a general chat.")
#             pass # final_prompt is already set to the original prompt
    
#     # If it's an existing conversation, use its history
#     else:
#         # ... your existing logic for fetching and formatting history from MongoDB ...
#         # This part remains the same.
#         conv_id = ObjectId(request.conversation_id)
#         conversation = await mongo_db.conversations.find_one(
#             {"_id": conv_id, "user_id": str(current_user.id)}
#         )
#         if conversation and "messages" in conversation:
#             print(f"Found conversation history with {len(conversation['messages'])} messages.")
#             # Note: This simple history format doesn't include the RAG context.
#             # A more advanced implementation might store the context with the first message.
#             final_prompt = format_prompt_with_history(request.prompt, conversation["messages"])

#     # --- Generate response and save to DB (this part is mostly the same) ---
#     print(f"Sending final prompt to Ollama:\n--- START ---\n{final_prompt}\n--- END ---")
#     response_text = await ollama_client.generate(prompt=final_prompt)
    
#     # Save the new exchange to MongoDB
#     new_message_exchange = [
#         {"role": "user", "message": request.prompt},
#         {"role": "ai", "message": response_text}
#     ]
    
#     if request.conversation_id:
#         conversation_id_str = request.conversation_id
#         await mongo_db.conversations.update_one(
#             {"_id": ObjectId(conversation_id_str)},
#             {"$push": {"messages": {"$each": new_message_exchange}}}
#         )
#     else:
#         new_convo_doc = {
#             "user_id": str(current_user.id), 
#             "messages": new_message_exchange, 
#             "created_at": datetime.datetime.now(datetime.timezone.utc)
#         }
#         result = await mongo_db.conversations.insert_one(new_convo_doc)
#         conversation_id_str = str(result.inserted_id)
        
#     print(f"Successfully saved/updated conversation. ID: {conversation_id_str}")
#     return ChatResponse(response=response_text, conversation_id=conversation_id_str)

# backend/api/chat.py
# import datetime
# from fastapi import APIRouter, Depends
# from motor.motor_asyncio import AsyncIOMotorClient
# from bson import ObjectId

# # --- LangChain Imports ---
# from langchain_community.vectorstores.pgvector import PGVector # <-- REVERT THIS IMPORT
# from langchain_ollama import ChatOllama, OllamaEmbeddings
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.runnables import RunnablePassthrough
# from langchain_core.output_parsers import StrOutputParser

# # --- Local Imports ---
# from backend.db.session import SYNC_DATABASE_URL # Import the SYNC URL for PGVector
# from backend.schemas.chat_schema import ChatRequest, ChatResponse
# from backend.api.auth_utils import get_current_user
# from backend.models.user import User
# from backend.db.mongodb import get_mongo_db

# router = APIRouter()

# # --- 1. RAG Chain Setup ---

# # This prompt template is key. It structures the input for the LLM.
# RAG_PROMPT_TEMPLATE = """
# You are an expert assistant. Use the following pieces of retrieved context to answer the user's question.
# If you don't know the answer from the provided context, just say that you don't have enough information from the document(s).

# CONTEXT:
# {context}

# QUESTION:
# {question}

# ANSWER:
# """

# # --- RAG Setup ---
# OLLAMA_BASE_URL = "http://ollama:11434"

# # Initialize the major components of our RAG chain
# llm = ChatOllama(model="llama3:8b", temperature=0, base_url=OLLAMA_BASE_URL)
# embeddings = OllamaEmbeddings(model="nomic-embed-text", base_url=OLLAMA_BASE_URL)
# vectorstore = PGVector(
#     connection_string=SYNC_DATABASE_URL,
#     embedding_function=embeddings,
# )

# # The retriever is the component that performs the similarity search.
# # We can configure it to, for example, only return the top 3 documents (k=3).
# retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# # The prompt template component will receive the context and question.
# prompt_template = ChatPromptTemplate.from_template(RAG_PROMPT_TEMPLATE)


# # --- 2. The RAG Chain Definition using LangChain Expression Language (LCEL) ---
# # This is the core of our new retrieval logic. It declaratively pipes components together.
# rag_chain = (
#     # The first part of the chain runs two actions in parallel:
#     # 1. The 'retriever' is called with the user's question.
#     # 2. The user's question is passed through using `RunnablePassthrough`.
#     # The results are gathered into a dictionary with keys "context" and "question".
#     {"context": retriever, "question": RunnablePassthrough()}
    
#     # The dictionary from the previous step is "piped" into our prompt template.
#     | prompt_template
    
#     # The formatted prompt is "piped" into the LLM.
#     | llm
    
#     # The LLM's response object is "piped" into a simple string parser.
#     | StrOutputParser()
# )


# @router.post("/chat", response_model=ChatResponse)
# async def handle_chat_request(
#     request: ChatRequest,
#     current_user: User = Depends(get_current_user),
#     mongo_db: AsyncIOMotorClient = Depends(get_mongo_db),
# ):
#     """
#     Handles a chat request using a LangChain RAG chain for new conversations.
#     For existing conversations, it will need to be adapted.
#     """
#     print(f"Handling chat request for user: {current_user.email}")
    
#     # For now, we'll simplify and assume every request can be a new RAG chat.
#     # Re-integrating MongoDB history with this chain is a more advanced topic.
    
#     # Invoke the RAG chain with the user's prompt.
#     # LangChain handles the retrieval, prompting, and generation in this single call.
#     print(f"Invoking RAG chain with question: '{request.prompt}'")
#     response_text = rag_chain.invoke(request.prompt)
#     print(f"RAG chain returned response.")
    
#     # --- MongoDB Saving Logic (remains the same) ---

#     # We will create a new conversation for each RAG query for simplicity.
#     new_convo_doc = {
#         "user_id": str(current_user.id), 
#         "messages": [
#             {"role": "user", "message": request.prompt},
#             {"role": "ai", "message": response_text}
#         ],
#         "created_at": datetime.datetime.now(datetime.timezone.utc)
#     }
#     result = await mongo_db.conversations.insert_one(new_convo_doc)
#     conversation_id_str = str(result.inserted_id)
        
#     print(f"Successfully created new RAG conversation. ID: {conversation_id_str}")
#     return ChatResponse(response=response_text, conversation_id=conversation_id_str)
# backend/api/chat.py
# import datetime
# from fastapi import APIRouter, Depends, HTTPException
# from motor.motor_asyncio import AsyncIOMotorClient
# import asyncio
# from bson import ObjectId
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.future import select

# # LangChain Imports
# from langchain_community.vectorstores.pgvector import PGVector
# from langchain_ollama import ChatOllama, OllamaEmbeddings
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.runnables import RunnablePassthrough
# from langchain_core.output_parsers import StrOutputParser

# # Local Imports
# from backend.db.session import get_db, SYNC_DATABASE_URL
# from backend.models.file_metadata import FileMetadata
# from backend.schemas.chat_schema import ChatRequest, ChatResponse
# from backend.api.auth_utils import get_current_user
# from backend.models.user import User
# from backend.db.mongodb import get_mongo_db

# router = APIRouter()

# # --- RAG Setup ---
# OLLAMA_BASE_URL = "http://ollama:11434"
# RAG_PROMPT_TEMPLATE = """
# You are an expert assistant. Use the following pieces of retrieved context to answer the user's question.
# If you don't know the answer from the provided context, just say that you don't have enough information.

# CONTEXT:
# {context}

# QUESTION:
# {question}

# ANSWER:
# """

# llm = ChatOllama(model="llama3:8b", temperature=0, base_url=OLLAMA_BASE_URL)
# embeddings = OllamaEmbeddings(model="nomic-embed-text", base_url=OLLAMA_BASE_URL)
# prompt_template = ChatPromptTemplate.from_template(RAG_PROMPT_TEMPLATE)
# output_parser = StrOutputParser()

# @router.post("/chat", response_model=ChatResponse)
# async def handle_chat_request(
#     request: ChatRequest,
#     current_user: User = Depends(get_current_user),
#     mongo_db: AsyncIOMotorClient = Depends(get_mongo_db),
#     # sql_db: AsyncSession = Depends(get_db), # Add back the SQL DB session
# ):
#     print(f"Handling chat request for user: {current_user.email}")

#       # Check if a specific file_id was provided for RAG
#     if request.file_id:
#         print(f"File ID '{request.file_id}' provided. Performing targeted RAG.")
        
#         # Security check: Ensure the file belongs to the current user
#         stmt = select(FileMetadata).where(
#             FileMetadata.id == request.file_id, 
#             FileMetadata.user_id == current_user.id
#         )
#         result = await sql_db.execute(stmt)
#         target_file = result.scalars().first()

#         if not target_file:
#             raise HTTPException(status_code=404, detail="File not found or permission denied.")

#         # Wait for the file to be processed. This is a simple "polling" mechanism.
#         # A more advanced system would use WebSockets or a proper task queue (Celery).
#         for _ in range(10): # Try for 10 seconds
#             if target_file.processing_status == "completed":
#                 break
#             print(f"File '{target_file.id}' is still processing. Waiting 1 second...")
#             await asyncio.sleep(1)
#             await sql_db.refresh(target_file)
        
#         if target_file.processing_status != "completed":
#              raise HTTPException(status_code=400, detail="File is still processing. Please try again in a moment.")

#         # Initialize a PGVector store pointed *specifically to this file's collection*.
#         vectorstore = PGVector(
#             connection_string=SYNC_DATABASE_URL,
#             embedding_function=embeddings,
#             # collection_name=str(target_file.id),
#         )
#         # retriever = vectorstore.as_retriever()
#         retriever = vectorstore.as_retriever(
#         search_kwargs={
#             "k": 5, # Retrieve top 5 most relevant chunks
#             "filter": {"user_id": str(current_user.id)}
#         }
#     )

#         rag_chain = (
#             {"context": retriever, "question": RunnablePassthrough()}
#             | prompt_template | llm | StrOutputParser()
#         )

#         print(f"Invoking universal RAG chain with question: '{request.prompt}'")
#         response_text = rag_chain.invoke(request.prompt)

#     else:
#         # If no file_id, handle as a standard chatbot or continued conversation
#         print("No file_id provided. Using LLM as a standard chatbot.")
#         # Here you can add back the MongoDB history logic if desired
#         response_text = llm.invoke(request.prompt).content

#     # --- MongoDB Saving Logic ---
#     new_convo_doc = {
#         "user_id": str(current_user.id), 
#         "messages": [
#             {"role": "user", "message": request.prompt},
#             {"role": "ai", "message": response_text}
#         ],
#         "created_at": datetime.datetime.now(datetime.timezone.utc)
#     }
#     # ... (the rest of the mongo logic is the same)
#     result = await mongo_db.conversations.insert_one(new_convo_doc)
#     conversation_id_str = str(result.inserted_id)
        
#     print(f"Successfully created new RAG conversation. ID: {conversation_id_str}")
#     return ChatResponse(response=response_text, conversation_id=conversation_id_str)

# backend/api/chat.py
# import datetime
# import asyncio
# from fastapi import APIRouter, Depends, HTTPException
# from motor.motor_asyncio import AsyncIOMotorClient
# from bson import ObjectId
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.future import select

# # LangChain Imports
# from langchain_community.vectorstores.pgvector import PGVector
# from langchain_ollama import ChatOllama, OllamaEmbeddings
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.runnables import RunnablePassthrough
# from langchain_core.output_parsers import StrOutputParser

# # Local Imports
# from backend.db.session import get_db, SYNC_DATABASE_URL
# from backend.models.file_metadata import FileMetadata
# from backend.schemas.chat_schema import ChatRequest, ChatResponse
# from backend.api.auth_utils import get_current_user
# from backend.models.user import User
# from backend.db.mongodb import get_mongo_db

# router = APIRouter()

# # --- RAG Setup ---
# OLLAMA_BASE_URL = "http://ollama:11434"
# RAG_PROMPT_TEMPLATE = """
# You are an expert assistant. Use the following pieces of retrieved context to answer the user's question.
# If you don't know the answer from the provided context, just say that you don't have enough information from the document.

# CONTEXT:
# {context}

# QUESTION:
# {question}

# ANSWER:
# """

# llm = ChatOllama(model="llama3:8b", temperature=0, base_url=OLLAMA_BASE_URL)
# embeddings = OllamaEmbeddings(model="nomic-embed-text", base_url=OLLAMA_BASE_URL)
# prompt_template = ChatPromptTemplate.from_template(RAG_PROMPT_TEMPLATE)
# output_parser = StrOutputParser()

# @router.post("/chat", response_model=ChatResponse)
# async def handle_chat_request(
#     request: ChatRequest,
#     current_user: User = Depends(get_current_user),
#     mongo_db: AsyncIOMotorClient = Depends(get_mongo_db),
#     sql_db: AsyncSession = Depends(get_db), # Add back the SQL DB session
# ):
#     print(f"Handling chat request for user: {current_user.email}")

#     # Check if a specific file_id was provided for RAG
#     if request.file_id:
#         print(f"File ID '{request.file_id}' provided. Performing targeted RAG.")
        
#         stmt = select(FileMetadata).where(FileMetadata.id == request.file_id, FileMetadata.user_id == current_user.id)
#         result = await sql_db.execute(stmt)
#         target_file = result.scalars().first()

#         if not target_file:
#             raise HTTPException(status_code=404, detail="File not found or permission denied.")

#         # Polling loop to wait for processing to finish
#         for _ in range(10):
#             if target_file.processing_status == "completed": break
#             print(f"File '{target_file.id}' is still processing. Waiting 1 second...")
#             await asyncio.sleep(1)
#             await sql_db.refresh(target_file)
        
#         if target_file.processing_status != "completed":
#              raise HTTPException(status_code=400, detail="File is still processing. Please try again.")

#         # Initialize PGVector pointed *specifically to this file's collection*.
#         vectorstore = PGVector(
#             connection_string=SYNC_DATABASE_URL,
#             embedding_function=embeddings,
#             collection_name=str(target_file.id),
#         )
        
#         # This retriever will now search ONLY within the correct collection.
#         retriever = vectorstore.as_retriever()

#         rag_chain = (
#             {"context": retriever, "question": RunnablePassthrough()}
#             | prompt_template | llm | output_parser
#         )
        
#         response_text = rag_chain.invoke(request.prompt)

#     else:
#         # If no file_id, handle as a standard chatbot.
#         print("No file_id provided. Using LLM as a standard chatbot.")
#         response_text = llm.invoke(request.prompt).content

#     # --- MongoDB Saving Logic ---
#     new_convo_doc = {
#         "user_id": str(current_user.id), 
#         "messages": [
#             {"role": "user", "message": request.prompt},
#             {"role": "ai", "message": response_text}
#         ],
#         "created_at": datetime.datetime.now(datetime.timezone.utc)
#     }
#     result = await mongo_db.conversations.insert_one(new_convo_doc)
#     conversation_id_str = str(result.inserted_id)
        
#     print(f"Successfully created new RAG conversation. ID: {conversation_id_str}")
#     return ChatResponse(response=response_text, conversation_id=conversation_id_str)

# backend/api/chat.py
# import datetime
# import asyncio
# from fastapi import APIRouter, Depends
# from motor.motor_asyncio import AsyncIOMotorClient
# from bson import ObjectId

# # LangChain Imports
# from langchain_community.vectorstores.pgvector import PGVector
# from langchain_ollama import ChatOllama, OllamaEmbeddings
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.runnables import RunnablePassthrough
# from langchain_core.output_parsers import StrOutputParser

# # Local Imports
# from backend.db.session import SYNC_DATABASE_URL
# from backend.schemas.chat_schema import ChatRequest, ChatResponse
# from backend.api.auth_utils import get_current_user
# from backend.models.user import User
# from backend.db.mongodb import get_mongo_db

# router = APIRouter()

# # --- RAG Setup ---
# OLLAMA_BASE_URL = "http://ollama:11434"
# RAG_PROMPT_TEMPLATE = """
# You are an expert assistant. Use ONLY the following pieces of context to answer the user's question.
# If the answer is not in the context, just say you don't have enough information from the documents.

# CONTEXT:
# {context}

# QUESTION:
# {question}

# ANSWER:
# """

# # Initialize major components
# llm = ChatOllama(model="llama3:8b", temperature=0, base_url=OLLAMA_BASE_URL)
# embeddings = OllamaEmbeddings(model="nomic-embed-text", base_url=OLLAMA_BASE_URL)
# prompt_template = ChatPromptTemplate.from_template(RAG_PROMPT_TEMPLATE)
# output_parser = StrOutputParser()

# @router.post("/chat", response_model=ChatResponse)
# async def handle_chat_request(
#     request: ChatRequest,
#     current_user: User = Depends(get_current_user),
#     mongo_db: AsyncIOMotorClient = Depends(get_mongo_db),
# ):
#     """
#     Handles a chat request. It always attempts to use RAG by searching across
#     all of the current user's documents for relevant context.
#     """
#     print(f"Handling chat request for user: {current_user.email}")

#     # --- Universal RAG Logic ---
#     # 1. Initialize the vector store to search the default collection.
#     vectorstore = PGVector(
#         connection_string=SYNC_DATABASE_URL,
#         embedding_function=embeddings,
#     )

#     # 2. Create a retriever that filters by the current user's ID.
#     # The 'filter' argument will look for a 'user_id' key in the metadata of each chunk.
#     # This is the key to multi-tenancy and true knowledge retention.
#     retriever = vectorstore.as_retriever(
#         search_kwargs={
#             "k": 5, # Retrieve top 5 most relevant chunks from ALL documents.
#             "filter": {"user_id": str(current_user.id)}
#         }
#     )

#     # 3. Define the full RAG chain.
#     rag_chain = (
#         {"context": retriever, "question": RunnablePassthrough()}
#         | prompt_template
#         | llm
#         | output_parser
#     )
    
#     # 4. Invoke the chain. It now automatically searches all documents
#     # belonging to the current user for relevant context.
#     print(f"Invoking universal RAG chain for user '{current_user.id}' with question: '{request.prompt}'")
#     response_text = rag_chain.invoke(request.prompt)

#     # --- MongoDB Saving Logic ---
#     # This logic can be simplified now that every query is a new RAG conversation.
#     new_convo_doc = {
#         "user_id": str(current_user.id), 
#         "messages": [
#             {"role": "user", "message": request.prompt},
#             {"role": "ai", "message": response_text}
#         ],
#         "created_at": datetime.datetime.now(datetime.timezone.utc)
#     }
#     result = await mongo_db.conversations.insert_one(new_convo_doc)
#     conversation_id_str = str(result.inserted_id)
        
#     print(f"Successfully created new RAG conversation. ID: {conversation_id_str}")
#     return ChatResponse(response=response_text, conversation_id=conversation_id_str)
#chat.py
# import datetime
# import asyncio
# from fastapi import APIRouter, Depends
# from motor.motor_asyncio import AsyncIOMotorClient
# from bson import ObjectId

# # LangChain Imports
# from langchain_community.vectorstores.pgvector import PGVector
# from langchain_ollama import ChatOllama, OllamaEmbeddings
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.runnables import RunnablePassthrough
# from langchain_core.output_parsers import StrOutputParser

# # Local Imports
# from backend.db.session import SYNC_DATABASE_URL
# from backend.schemas.chat_schema import ChatRequest, ChatResponse
# from backend.api.auth_utils import get_current_user
# from backend.models.user import User
# from backend.db.mongodb import get_mongo_db

# router = APIRouter()

# # --- RAG Setup ---
# OLLAMA_BASE_URL = "http://ollama:11434"
# RAG_PROMPT_TEMPLATE = """
# You are an expert assistant. Use ONLY the following pieces of context to answer the user's question.
# If the answer is not in the context, just say you don't have enough information from the documents.

# CONTEXT:
# {context}

# QUESTION:
# {question}

# ANSWER:
# """
# rag_prompt_template = ChatPromptTemplate.from_template(RAG_PROMPT_TEMPLATE)

# # 2. A general prompt for when we DON'T have context
# GENERAL_PROMPT_TEMPLATE = """
# You are a helpful AI assistant. Answer the user's question based on your own knowledge.

# QUESTION:
# {question}

# ANSWER:
# """
# general_prompt_template = ChatPromptTemplate.from_template(GENERAL_PROMPT_TEMPLATE)

# # Initialize major components
# llm = ChatOllama(model="llama3:8b", temperature=0, base_url=OLLAMA_BASE_URL)
# embeddings = OllamaEmbeddings(model="nomic-embed-text", base_url=OLLAMA_BASE_URL)
# # prompt_template = ChatPromptTemplate.from_template(RAG_PROMPT_TEMPLATE)
# output_parser = StrOutputParser()

# @router.post("/chat", response_model=ChatResponse)
# async def handle_chat_request(
#     request: ChatRequest,
#     current_user: User = Depends(get_current_user),
#     mongo_db: AsyncIOMotorClient = Depends(get_mongo_db),
# ):
#     print(f"Handling chat request for user: {current_user.email}")

#     vectorstore = PGVector(
#         connection_string=SYNC_DATABASE_URL,
#         embedding_function=embeddings,
#     )

#     # # --- THE FIX: Use a Stricter Retriever ---
#     # # We now use a different search type.
#     # retriever = vectorstore.as_retriever(
#     #     search_type="similarity_score_threshold",
#     #     search_kwargs={
#     #         "k": 3, # Still get up to 3 documents...
#     #         "score_threshold": 0.5, # ...but ONLY if their similarity score is above this value.
#     #         "filter": {"user_id": str(current_user.id)}
#     #     }
#     # )

#     # --- DYNAMIC FILTERING LOGIC ---
#     # Start with the mandatory user_id filter
#     retriever_filter = {"user_id": str(current_user.id)}

#     # If the user selected specific files, add a file_id filter.
#     # We use the '$in' operator to match any of the provided IDs.
#     if request.selected_file_ids:
#         # PGVector expects a list of strings for the filter
#         string_file_ids = [str(uuid) for uuid in request.selected_file_ids]
#         retriever_filter["file_id"] = {"$in": string_file_ids}
#         print(f"Applying filter: {retriever_filter}")

#     # Use the dynamically created filter in the retriever
#     retriever = vectorstore.as_retriever(
#         search_type="similarity_score_threshold",
#         search_kwargs={
#             "k": 5, # You can adjust k
#             "score_threshold": 0.45,
#             "filter": retriever_filter # <-- USE THE DYNAMIC FILTER
#         }
#     )

#     # Step 1: Retrieve documents FIRST
#     # The retriever will now return an empty list for "2+2" because no chunks meet the threshold.
#     retrieved_docs = retriever.invoke(request.prompt)
    
#     # Step 2: Check if any documents were found and format the context
#     if retrieved_docs:
#         print(f"📚 Found {len(retrieved_docs)} relevant document(s) above threshold. Using RAG prompt.")
#         context = "\n\n---\n\n".join([doc.page_content for doc in retrieved_docs])
#         prompt = rag_prompt_template.format(context=context, question=request.prompt)
#     else:
#         print("📚 No relevant documents found above threshold. Using general knowledge prompt.")
#         prompt = general_prompt_template.format(question=request.prompt)
        
#     # Step 3: Invoke the LLM with the correct prompt
#     generation_chain = (llm | output_parser)
    
#     print(f"Invoking LLM with final prompt...")
#     response_text = generation_chain.invoke(prompt)

#     # --- MongoDB Saving Logic ---
#     # This logic can be simplified now that every query is a new RAG conversation.
#     new_convo_doc = {
#         "user_id": str(current_user.id), 
#         "messages": [
#             {"role": "user", "message": request.prompt},
#             {"role": "ai", "message": response_text}
#         ],
#         "created_at": datetime.datetime.now(datetime.timezone.utc)
#     }
#     result = await mongo_db.conversations.insert_one(new_convo_doc)
#     conversation_id_str = str(result.inserted_id)
        
#     print(f"Successfully created new RAG conversation. ID: {conversation_id_str}")
#     return ChatResponse(response=response_text, conversation_id=conversation_id_str)

# import datetime
# import asyncio
# from fastapi import APIRouter, Depends
# from motor.motor_asyncio import AsyncIOMotorClient
# from bson import ObjectId

# # LangChain Imports
# from langchain_community.vectorstores.pgvector import PGVector
# from langchain_ollama import ChatOllama, OllamaEmbeddings
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.runnables import RunnablePassthrough
# from langchain_core.output_parsers import StrOutputParser

# # Local Imports
# from backend.db.session import SYNC_DATABASE_URL
# from backend.schemas.chat_schema import ChatRequest, ChatResponse
# from backend.api.auth_utils import get_current_user
# from backend.models.user import User
# from backend.db.mongodb import get_mongo_db

# router = APIRouter()

# # --- RAG Setup ---
# OLLAMA_BASE_URL = "http://ollama:11434"
# RAG_PROMPT_TEMPLATE = """
# You are an expert assistant. Use ONLY the following pieces of context to answer the user's question.
# If the answer is not in the context, just say you don't have enough information from the documents.

# CONTEXT:
# {context}

# QUESTION:
# {question}

# ANSWER:
# """
# rag_prompt_template = ChatPromptTemplate.from_template(RAG_PROMPT_TEMPLATE)

# # 2. A general prompt for when we DON'T have context
# GENERAL_PROMPT_TEMPLATE = """
# You are a helpful AI assistant. Answer the user's question based on your own knowledge.

# QUESTION:
# {question}

# ANSWER:
# """
# general_prompt_template = ChatPromptTemplate.from_template(GENERAL_PROMPT_TEMPLATE)

# # Initialize major components
# llm = ChatOllama(model="llama3:8b", temperature=0, base_url=OLLAMA_BASE_URL)
# embeddings = OllamaEmbeddings(model="nomic-embed-text", base_url=OLLAMA_BASE_URL)
# # prompt_template = ChatPromptTemplate.from_template(RAG_PROMPT_TEMPLATE)
# output_parser = StrOutputParser()

# @router.post("/chat", response_model=ChatResponse)
# async def handle_chat_request(
#     request: ChatRequest,
#     current_user: User = Depends(get_current_user),
#     mongo_db: AsyncIOMotorClient = Depends(get_mongo_db),
# ):
#     print(f"Handling chat request for user: {current_user.email}")

#     vectorstore = PGVector(
#         connection_string=SYNC_DATABASE_URL,
#         embedding_function=embeddings,
#     )

#     # # --- THE FIX: Use a Stricter Retriever ---
#     # # We now use a different search type.
#     # retriever = vectorstore.as_retriever(
#     #     search_type="similarity_score_threshold",
#     #     search_kwargs={
#     #         "k": 3, # Still get up to 3 documents...
#     #         "score_threshold": 0.5, # ...but ONLY if their similarity score is above this value.
#     #         "filter": {"user_id": str(current_user.id)}
#     #     }
#     # )

#     # --- DYNAMIC FILTERING LOGIC ---
#     # Start with the mandatory user_id filter
#     retriever_filter = {"user_id": str(current_user.id)}

#     # If the user selected specific files, add a file_id filter.
#     # We use the '$in' operator to match any of the provided IDs.
#     if request.selected_file_ids:
#         # PGVector expects a list of strings for the filter
#         string_file_ids = [str(uuid) for uuid in request.selected_file_ids]
#         retriever_filter["file_id"] = {"$in": string_file_ids}
#         print(f"Applying filter: {retriever_filter}")

#     # Use the dynamically created filter in the retriever
#     retriever = vectorstore.as_retriever(
#         search_type="similarity_score_threshold",
#         search_kwargs={
#             "k": 5, # You can adjust k
#             "score_threshold": 0.45,
#             "filter": retriever_filter # <-- USE THE DYNAMIC FILTER
#         }
#     )

#     # Step 1: Retrieve documents FIRST
#     # The retriever will now return an empty list for "2+2" because no chunks meet the threshold.
#     retrieved_docs = retriever.invoke(request.prompt)
    
#     # Step 2: Check if any documents were found and format the context
#     if retrieved_docs:
#         print(f"📚 Found {len(retrieved_docs)} relevant document(s) above threshold. Using RAG prompt.")
#         context = "\n\n---\n\n".join([doc.page_content for doc in retrieved_docs])
#         prompt = rag_prompt_template.format(context=context, question=request.prompt)
#     else:
#         print("📚 No relevant documents found above threshold. Using general knowledge prompt.")
#         prompt = general_prompt_template.format(question=request.prompt)
        
#     # Step 3: Invoke the LLM with the correct prompt
#     generation_chain = (llm | output_parser)
    
#     print(f"Invoking LLM with final prompt...")
#     response_text = generation_chain.invoke(prompt)

#     # --- MongoDB Saving Logic ---
#     # This logic can be simplified now that every query is a new RAG conversation.
#     new_convo_doc = {
#         "user_id": str(current_user.id), 
#         "messages": [
#             {"role": "user", "message": request.prompt},
#             {"role": "ai", "message": response_text}
#         ],
#         "created_at": datetime.datetime.now(datetime.timezone.utc)
#     }
#     result = await mongo_db.conversations.insert_one(new_convo_doc)
#     conversation_id_str = str(result.inserted_id)
        
#     print(f"Successfully created new RAG conversation. ID: {conversation_id_str}")
#     return ChatResponse(response=response_text, conversation_id=conversation_id_str)
# import datetime
# from fastapi import APIRouter, Depends, HTTPException
# from motor.motor_asyncio import AsyncIOMotorClient
# from bson import ObjectId

# # --- LangChain Imports ---
# from langchain_core.prompts import PromptTemplate
# from langchain_core.output_parsers import StrOutputParser
# from langchain.chains import LLMChain
# from langchain_community.vectorstores.pgvector import PGVector
# from langchain_ollama import ChatOllama, OllamaEmbeddings
# from langchain_community.cross_encoders import HuggingFaceCrossEncoder
# from langchain.retrievers.document_compressors import CrossEncoderReranker
# from langchain.retrievers.contextual_compression import ContextualCompressionRetriever

# # --- Local Imports ---
# from backend.db.session import SYNC_DATABASE_URL
# from backend.schemas.chat_schema import ChatRequest, ChatResponse
# from backend.api.auth_utils import get_current_user
# from backend.models.user import User
# from backend.db.mongodb import get_mongo_db

# # --- Environment Setup & Constants ---
# router = APIRouter()
# OLLAMA_BASE_URL = "http://ollama:11434"

# # --- Prompt Templates ---
# REWRITE_PROMPT_TEMPLATE = """
# Based on the chat history below, formulate a standalone question that can be understood
# without the chat history. Do NOT answer the question, just reformulate it if needed,
# otherwise return it as is.

# Chat History:
# {chat_history}

# Latest User Question:
# {question}

# Standalone Question:
# """
# rewrite_prompt = PromptTemplate.from_template(REWRITE_PROMPT_TEMPLATE)

# RAG_PROMPT_TEMPLATE = """
# You are an expert assistant. Use ONLY the following pieces of context to answer the user's question.
# If the answer is not in the context, just say you don't have enough information from the documents.

# CONTEXT:
# {context}

# QUESTION:
# {question}

# ANSWER:
# """
# rag_prompt_template = PromptTemplate.from_template(RAG_PROMPT_TEMPLATE)

# # --- Initialize Core Components ---
# print("Initializing LLM, embeddings, and re-ranker models...")
# llm = ChatOllama(model="llama3:8b", temperature=0, base_url=OLLAMA_BASE_URL)
# embeddings = OllamaEmbeddings(model="nomic-embed-text", base_url=OLLAMA_BASE_URL)
# output_parser = StrOutputParser()

# # --- THIS IS THE CORRECTED LINE ---
# # Initialize the local Cross-Encoder model with the full, namespaced identifier.
# cross_encoder_model = HuggingFaceCrossEncoder(model_name="cross-encoder/ms-marco-MiniLM-L-6-v2")
# print("Models initialized successfully.")


# @router.post("/chat", response_model=ChatResponse)
# async def handle_chat_request(
#     request: ChatRequest,
#     current_user: User = Depends(get_current_user),
#     mongo_db: AsyncIOMotorClient = Depends(get_mongo_db),
# ):
#     print(f"\n--- New Chat Request for user: {current_user.email} ---")
#     print(f"Original question: '{request.prompt}'")

#     # --- 1. QUERY REWRITING STAGE ---
#     chat_history_str = ""
#     if request.conversation_id:
#         if not ObjectId.is_valid(request.conversation_id):
#             raise HTTPException(status_code=400, detail="Invalid conversation_id format.")
        
#         convo = await mongo_db.conversations.find_one(
#             {"_id": ObjectId(request.conversation_id), "user_id": str(current_user.id)}
#         )
#         if convo and convo.get("messages"):
#             messages = [f"{msg['role']}: {msg['message']}" for msg in convo["messages"]]
#             chat_history_str = "\n".join(messages)

#     query_rewriter_chain = LLMChain(llm=llm, prompt=rewrite_prompt, output_parser=StrOutputParser())
#     # The output of ainvoke is a dictionary containing all keys from the chain.
#     response_dict = await query_rewriter_chain.ainvoke({
#         "chat_history": chat_history_str,
#         "question": request.prompt
#     })
#     # We need to extract the actual text output from the 'text' key.
#     rewritten_query = response_dict['text']
#     print(f"Rewritten query for retrieval: '{rewritten_query}'")

#     # --- 2. RETRIEVAL & RE-RANKING STAGE ---
#     vectorstore = PGVector(connection_string=SYNC_DATABASE_URL, embedding_function=embeddings)
    
#     base_retriever = vectorstore.as_retriever(
#         search_type="similarity",
#         search_kwargs={"k": 20, "filter": {"user_id": str(current_user.id)}}
#     )
    
#     reranker = CrossEncoderReranker(model=cross_encoder_model, top_n=5)
    
#     compression_retriever = ContextualCompressionRetriever(
#         base_compressor=reranker, 
#         base_retriever=base_retriever
#     )

#     final_context_docs = await compression_retriever.ainvoke(rewritten_query)
#     print(f"Retrieved and re-ranked to {len(final_context_docs)} final documents.")

#     # --- 3. GENERATION STAGE ---
#     response_text = ""
#     if final_context_docs:
#         print("📚 Found relevant documents. Generating answer with RAG.")
#         context_str = "\n\n---\n\n".join([doc.page_content for doc in final_context_docs])
#         rag_chain = rag_prompt_template | llm | output_parser
#         response_text = await rag_chain.ainvoke({
#             "context": context_str,
#             "question": rewritten_query
#         })
#     else:
#         print("📚 No relevant documents found. Generating answer from general knowledge.")
#         response_text = await llm.ainvoke(rewritten_query)

#     # --- 4. SAVE TO MONGODB & RETURN RESPONSE ---
#     convo_id_obj = ObjectId(request.conversation_id) if request.conversation_id else ObjectId()
#     new_messages = [
#         {"role": "user", "message": request.prompt},
#         {"role": "ai", "message": response_text}
#     ]
    
#     await mongo_db.conversations.update_one(
#         {"_id": convo_id_obj, "user_id": str(current_user.id)},
#         {
#             "$push": {"messages": {"$each": new_messages}},
#             "$setOnInsert": {
#                 "user_id": str(current_user.id),
#                 "created_at": datetime.datetime.now(datetime.timezone.utc)
#             }
#         },
#         upsert=True
#     )
        
#     print(f"Successfully saved to conversation. ID: {convo_id_obj}")
#     return ChatResponse(response=response_text, conversation_id=str(convo_id_obj))
# import datetime
# from fastapi import APIRouter, Depends, HTTPException
# from motor.motor_asyncio import AsyncIOMotorClient
# from bson import ObjectId

# # --- LangChain Imports ---
# from langchain_core.prompts import PromptTemplate
# from langchain_core.output_parsers import StrOutputParser
# from langchain.chains import LLMChain
# from langchain_community.vectorstores.pgvector import PGVector
# from langchain_ollama import ChatOllama, OllamaEmbeddings
# from langchain_community.cross_encoders import HuggingFaceCrossEncoder
# from langchain.retrievers.document_compressors import CrossEncoderReranker
# from langchain.retrievers.contextual_compression import ContextualCompressionRetriever

# # --- Local Imports ---
# from backend.db.session import SYNC_DATABASE_URL
# from backend.schemas.chat_schema import ChatRequest, ChatResponse
# from backend.api.auth_utils import get_current_user
# from backend.models.user import User
# from backend.db.mongodb import get_mongo_db

# # --- Environment Setup & Constants ---
# router = APIRouter()
# OLLAMA_BASE_URL = "http://ollama:11434"

# # --- Prompt Templates ---
# REWRITE_PROMPT_TEMPLATE = """
# Based on the chat history below, formulate a standalone question that can be understood
# without the chat history. Do NOT answer the question, just reformulate it if needed,
# otherwise return it as is.

# Chat History:
# {chat_history}

# Latest User Question:
# {question}

# Standalone Question:
# """
# rewrite_prompt = PromptTemplate.from_template(REWRITE_PROMPT_TEMPLATE)

# RAG_PROMPT_TEMPLATE = """
# You are an expert assistant. Use ONLY the following pieces of context to answer the user's question.
# If the answer is not in the context, just say you don't have enough information from the documents.

# CONTEXT:
# {context}

# QUESTION:
# {question}

# ANSWER:
# """
# rag_prompt_template = PromptTemplate.from_template(RAG_PROMPT_TEMPLATE)

# # --- Initialize Core Components ---
# print("Initializing LLM, embeddings, and re-ranker models...")
# embeddings = OllamaEmbeddings(model="nomic-embed-text", base_url=OLLAMA_BASE_URL)
# output_parser = StrOutputParser()

# # --- THIS IS THE CORRECTED LINE ---
# # Initialize the local Cross-Encoder model with the full, namespaced identifier.
# cross_encoder_model = HuggingFaceCrossEncoder(model_name="cross-encoder/ms-marco-MiniLM-L-6-v2")
# print("Models initialized successfully.")


# @router.post("/chat", response_model=ChatResponse)
# async def handle_chat_request(
#     request: ChatRequest,
#     current_user: User = Depends(get_current_user),
#     mongo_db: AsyncIOMotorClient = Depends(get_mongo_db),
# ):
#     print(f"\n--- New Chat Request for user: {current_user.email} ---")
#     print(f"Original question: '{request.prompt}'")
#     # --- NEW: Get model from request ---
#     model_name = request.selected_model
#     print(f"Using model: '{model_name}'")

#     llm = ChatOllama(model=model_name, temperature=0, base_url=OLLAMA_BASE_URL)

#     # --- 1. QUERY REWRITING STAGE ---
#     chat_history_str = ""
#     if request.conversation_id:
#         if not ObjectId.is_valid(request.conversation_id):
#             raise HTTPException(status_code=400, detail="Invalid conversation_id format.")
        
#         convo = await mongo_db.conversations.find_one(
#             {"_id": ObjectId(request.conversation_id), "user_id": str(current_user.id)}
#         )
#         if convo and convo.get("messages"):
#             messages = [f"{msg['role']}: {msg['message']}" for msg in convo["messages"]]
#             chat_history_str = "\n".join(messages)

#     query_rewriter_chain = LLMChain(llm=llm, prompt=rewrite_prompt, output_parser=StrOutputParser())
#     # The output of ainvoke is a dictionary containing all keys from the chain.
#     response_dict = await query_rewriter_chain.ainvoke({
#         "chat_history": chat_history_str,
#         "question": request.prompt
#     })
#     # We need to extract the actual text output from the 'text' key.
#     rewritten_query = response_dict['text']
#     print(f"Rewritten query for retrieval: '{rewritten_query}'")

#     # --- 2. RETRIEVAL & RE-RANKING STAGE ---
#     vectorstore = PGVector(connection_string=SYNC_DATABASE_URL, embedding_function=embeddings)
    
#     base_retriever = vectorstore.as_retriever(
#         search_type="similarity",
#         search_kwargs={"k": 20, "filter": {"user_id": str(current_user.id)}}
#     )
    
#     reranker = CrossEncoderReranker(model=cross_encoder_model, top_n=5)
    
#     compression_retriever = ContextualCompressionRetriever(
#         base_compressor=reranker, 
#         base_retriever=base_retriever
#     )

#     final_context_docs = await compression_retriever.ainvoke(rewritten_query)
#     print(f"Retrieved and re-ranked to {len(final_context_docs)} final documents.")

#     # --- 3. GENERATION STAGE ---
#     response_text = ""
#     if final_context_docs:
#         print("📚 Found relevant documents. Generating answer with RAG.")
#         context_str = "\n\n---\n\n".join([doc.page_content for doc in final_context_docs])
#         rag_chain = rag_prompt_template | llm | output_parser
#         response_text = await rag_chain.ainvoke({
#             "context": context_str,
#             "question": rewritten_query
#         })
#     else:
#         print("📚 No relevant documents found. Generating answer from general knowledge.")
#         response_text = await llm.ainvoke(rewritten_query)

#     # --- 4. SAVE TO MONGODB & RETURN RESPONSE ---
#     convo_id_obj = ObjectId(request.conversation_id) if request.conversation_id else ObjectId()
#     new_messages = [
#         {"role": "user", "message": request.prompt},
#         {"role": "ai", "message": response_text}
#     ]
    
#     await mongo_db.conversations.update_one(
#         {"_id": convo_id_obj, "user_id": str(current_user.id)},
#         {
#             "$push": {"messages": {"$each": new_messages}},
#             "$setOnInsert": {
#                 "user_id": str(current_user.id),
#                 "created_at": datetime.datetime.now(datetime.timezone.utc)
#             }
#         },
#         upsert=True
#     )
        
#     print(f"Successfully saved to conversation. ID: {convo_id_obj}")
#     return ChatResponse(response=response_text, conversation_id=str(convo_id_obj))
# import datetime
# from fastapi import APIRouter, Depends, HTTPException
# from motor.motor_asyncio import AsyncIOMotorClient
# from bson import ObjectId

# # --- LangChain Imports ---
# from langchain_core.prompts import PromptTemplate
# from langchain_core.output_parsers import StrOutputParser
# from langchain.chains import LLMChain
# from langchain_community.vectorstores.pgvector import PGVector
# from langchain_ollama import ChatOllama, OllamaEmbeddings
# from langchain_community.cross_encoders import HuggingFaceCrossEncoder
# from langchain.retrievers.document_compressors import CrossEncoderReranker
# from langchain.retrievers.contextual_compression import ContextualCompressionRetriever

# # --- Local Imports ---
# from backend.db.session import SYNC_DATABASE_URL
# from backend.schemas.chat_schema import ChatRequest, ChatResponse
# from backend.api.auth_utils import get_current_user
# from backend.models.user import User
# from backend.db.mongodb import get_mongo_db

# # --- Environment Setup & Constants ---
# router = APIRouter()
# OLLAMA_BASE_URL = "http://ollama:11434"

# # --- Prompt Templates ---
# # We still keep the default RAG prompt as a fallback
# DEFAULT_RAG_PROMPT_TEMPLATE = """
# You are an expert assistant. Use ONLY the following pieces of context to answer the user's question.
# If the answer is not in the context, just say you don't have enough information from the documents.

# CONTEXT:
# {context}

# QUESTION:
# {question}

# ANSWER:
# """
# default_rag_prompt = PromptTemplate.from_template(DEFAULT_RAG_PROMPT_TEMPLATE)

# # --- Initialize Core Components ---
# print("Initializing LLM, embeddings, and re-ranker models...")
# embeddings = OllamaEmbeddings(model="nomic-embed-text", base_url=OLLAMA_BASE_URL)
# output_parser = StrOutputParser()

# # --- THIS IS THE CORRECTED LINE ---
# # Initialize the local Cross-Encoder model with the full, namespaced identifier.
# cross_encoder_model = HuggingFaceCrossEncoder(model_name="cross-encoder/ms-marco-MiniLM-L-6-v2")
# print("Models initialized successfully.")


# @router.post("/chat", response_model=ChatResponse)
# async def handle_chat_request(
#     request: ChatRequest,
#     current_user: User = Depends(get_current_user),
#     mongo_db: AsyncIOMotorClient = Depends(get_mongo_db),
# ):
#     print(f"\n--- New Chat Request for user: {current_user.email} ---")
#     print(f"Original question: '{request.prompt}'")
#     # --- NEW: Get model from request ---
#     model_name = request.selected_model
#     print(f"Using model: '{model_name}'")

#     llm = ChatOllama(model=model_name, temperature=0, base_url=OLLAMA_BASE_URL)

#     # --- 1. QUERY REWRITING STAGE ---
#     chat_history_str = ""
#     if request.conversation_id:
#         if not ObjectId.is_valid(request.conversation_id):
#             raise HTTPException(status_code=400, detail="Invalid conversation_id format.")
        
#         convo = await mongo_db.conversations.find_one(
#             {"_id": ObjectId(request.conversation_id), "user_id": str(current_user.id)}
#         )
#         if convo and convo.get("messages"):
#             messages = [f"{msg['role']}: {msg['message']}" for msg in convo["messages"]]
#             chat_history_str = "\n".join(messages)

#     final_rag_prompt = default_rag_prompt
#     if request.custom_prompt_template:
#         print("✅ Using custom prompt template provided by user.")
#         try:
#             final_rag_prompt = PromptTemplate.from_template(request.custom_prompt_template)
#         except Exception as e:
#             print(f"⚠️ Warning: Invalid custom prompt template. Falling back to default. Error: {e}")

#     query_rewriter_chain = LLMChain(llm=llm, prompt=final_rag_prompt, output_parser=StrOutputParser())
#     # The output of ainvoke is a dictionary containing all keys from the chain.
#     response_dict = await query_rewriter_chain.ainvoke({
#         "chat_history": chat_history_str,
#         "question": request.prompt
#     })
#     # We need to extract the actual text output from the 'text' key.
#     rewritten_query = response_dict['text']
#     print(f"Rewritten query for retrieval: '{rewritten_query}'")

#     # --- 2. RETRIEVAL & RE-RANKING STAGE ---
#     vectorstore = PGVector(connection_string=SYNC_DATABASE_URL, embedding_function=embeddings)
    
#     base_retriever = vectorstore.as_retriever(
#         search_type="similarity",
#         search_kwargs={"k": 20, "filter": {"user_id": str(current_user.id)}}
#     )
    
#     reranker = CrossEncoderReranker(model=cross_encoder_model, top_n=5)
    
#     compression_retriever = ContextualCompressionRetriever(
#         base_compressor=reranker, 
#         base_retriever=base_retriever
#     )

#     final_context_docs = await compression_retriever.ainvoke(rewritten_query)
#     print(f"Retrieved and re-ranked to {len(final_context_docs)} final documents.")

#     # --- 3. GENERATION STAGE ---
#     response_text = ""
#     if final_context_docs:
#         print("📚 Found relevant documents. Generating answer with RAG.")
#         context_str = "\n\n---\n\n".join([doc.page_content for doc in final_context_docs])
#         # Use the final_rag_prompt variable here
#         rag_chain = final_rag_prompt | llm | output_parser
#         response_text = await rag_chain.ainvoke({"context": context_str, "question": rewritten_query})
#     else:
#         print("📚 No relevant documents found. Generating answer from general knowledge.")
#         response_text = await llm.ainvoke(rewritten_query)

#     # --- 4. SAVE TO MONGODB & RETURN RESPONSE ---
#     convo_id_obj = ObjectId(request.conversation_id) if request.conversation_id else ObjectId()
#     new_messages = [
#         {"role": "user", "message": request.prompt},
#         {"role": "ai", "message": response_text}
#     ]
    
#     await mongo_db.conversations.update_one(
#         {"_id": convo_id_obj, "user_id": str(current_user.id)},
#         {
#             "$push": {"messages": {"$each": new_messages}},
#             "$setOnInsert": {
#                 "user_id": str(current_user.id),
#                 "created_at": datetime.datetime.now(datetime.timezone.utc)
#             }
#         },
#         upsert=True
#     )
        
#     print(f"Successfully saved to conversation. ID: {convo_id_obj}")
#     return ChatResponse(response=response_text, conversation_id=str(convo_id_obj))
# import datetime
# import os
# from fastapi import APIRouter, Depends, HTTPException
# from motor.motor_asyncio import AsyncIOMotorClient
# from bson import ObjectId

# # --- LangChain Imports ---
# from langchain_core.prompts import PromptTemplate
# from langchain_core.output_parsers import StrOutputParser
# from langchain.chains import LLMChain
# from langchain_community.vectorstores.pgvector import PGVector
# from langchain_ollama import ChatOllama, OllamaEmbeddings
# from langchain_community.cross_encoders import HuggingFaceCrossEncoder
# from langchain.retrievers.document_compressors import CrossEncoderReranker
# from langchain.retrievers.contextual_compression import ContextualCompressionRetriever

# # --- Local Imports ---
# from backend.db.session import SYNC_DATABASE_URL
# from backend.schemas.chat_schema import ChatRequest, ChatResponse
# from backend.api.auth_utils import get_current_user
# from backend.models.user import User
# from backend.db.mongodb import get_mongo_db

# # --- Environment Setup & Constants ---
# router = APIRouter()
# OLLAMA_BASE_URL = os.getenv("OLLAMA_HOST", "http://ollama:11434")

# # --- Prompt Templates ---

# # This prompt is ONLY for rewriting the user's query and is always the same.
# REWRITE_PROMPT_TEMPLATE = """
# Based on the chat history below, formulate a standalone question that can be understood
# without the chat history. Do NOT answer the question, just reformulate it if needed,
# otherwise return it as is.

# Chat History:
# {chat_history}

# Latest User Question:
# {question}

# Standalone Question:
# """
# rewrite_prompt = PromptTemplate.from_template(REWRITE_PROMPT_TEMPLATE)

# # This is the default prompt for the main RAG task.
# DEFAULT_RAG_PROMPT_TEMPLATE = """
# You are an expert assistant. Use ONLY the following pieces of context to answer the user's question.
# If the answer is not in the context, just say you don't have enough information from the documents.

# CONTEXT:
# {context}

# QUESTION:
# {question}

# ANSWER:
# """
# default_rag_prompt = PromptTemplate.from_template(DEFAULT_RAG_PROMPT_TEMPLATE)

# # --- Initialize Models That Don't Change Per Request ---
# print("Initializing static models (embeddings, re-ranker)...")
# embeddings = OllamaEmbeddings(model="nomic-embed-text", base_url=OLLAMA_BASE_URL)
# cross_encoder_model = HuggingFaceCrossEncoder(model_name="cross-encoder/ms-marco-MiniLM-L-6-v2")
# output_parser = StrOutputParser()
# print("Static models initialized successfully.")


# @router.post("/chat", response_model=ChatResponse)
# async def handle_chat_request(
#     request: ChatRequest,
#     current_user: User = Depends(get_current_user),
#     mongo_db: AsyncIOMotorClient = Depends(get_mongo_db),
# ):
#     print(f"\n--- New Chat Request for user: {current_user.email} ---")
#     print(f"Original question: '{request.prompt}'")
#     model_name = request.selected_model
#     print(f"Using model: '{model_name}'")

#     # Dynamically instantiate the LLM for this specific request
#     llm = ChatOllama(model=model_name, temperature=0, base_url=OLLAMA_BASE_URL)

#     # --- 1. QUERY REWRITING STAGE ---
#     chat_history_str = ""
#     if request.conversation_id:
#         convo = await mongo_db.conversations.find_one({"_id": ObjectId(request.conversation_id), "user_id": str(current_user.id)})
#         if convo and convo.get("messages"):
#             messages = [f"{msg['role']}: {msg['message']}" for msg in convo["messages"]]
#             chat_history_str = "\n".join(messages)
            
#     # --- THIS IS THE FIX ---
#     # The rewriter chain should ALWAYS use the simple rewrite_prompt.
#     query_rewriter_chain = LLMChain(llm=llm, prompt=rewrite_prompt, output_parser=StrOutputParser())
#     response_dict = await query_rewriter_chain.ainvoke({
#         "chat_history": chat_history_str,
#         "question": request.prompt
#     })
#     rewritten_query = response_dict['text']
#     # --- END FIX ---
#     print(f"Rewritten query for retrieval: '{rewritten_query}'")

#     # --- 2. RETRIEVAL & RE-RANKING STAGE ---
#     # Determine which prompt to use for the main generation step
#     final_rag_prompt = default_rag_prompt
#     if request.custom_prompt_template:
#         print("✅ Using custom prompt template provided by user.")
#         try:
#             final_rag_prompt = PromptTemplate.from_template(request.custom_prompt_template)
#         except Exception as e:
#             print(f"⚠️ Warning: Invalid custom prompt template. Falling back to default. Error: {e}")
    
#     # (Retrieval logic is unchanged)
#     vectorstore = PGVector(connection_string=SYNC_DATABASE_URL, embedding_function=embeddings)
#     base_retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 20, "filter": {"user_id": str(current_user.id)}})
#     reranker = CrossEncoderReranker(model=cross_encoder_model, top_n=5)
#     compression_retriever = ContextualCompressionRetriever(base_compressor=reranker, base_retriever=base_retriever)
#     final_context_docs = await compression_retriever.ainvoke(rewritten_query)
#     print(f"Retrieved and re-ranked to {len(final_context_docs)} final documents.")

#     # --- 3. GENERATION STAGE ---
#     response_text = ""
#     if final_context_docs:
#         print("📚 Found relevant documents. Generating answer with RAG.")
#         context_str = "\n\n---\n\n".join([doc.page_content for doc in final_context_docs])
#         # The main RAG chain is now correctly built with the final_rag_prompt.
#         rag_chain = final_rag_prompt | llm | output_parser
#         response_text = await rag_chain.ainvoke({"context": context_str, "question": rewritten_query})
#     else:
#         print("📚 No relevant documents found. Generating answer from general knowledge.")
#         response_text = await llm.ainvoke(rewritten_query)

#     # --- 4. SAVE TO MONGODB & RETURN RESPONSE (Unchanged) ---
#     convo_id_obj = ObjectId(request.conversation_id) if request.conversation_id else ObjectId()
#     new_messages = [{"role": "user", "message": request.prompt}, {"role": "ai", "message": response_text}]
#     await mongo_db.conversations.update_one(
#         {"_id": convo_id_obj, "user_id": str(current_user.id)},
#         {"$push": {"messages": {"$each": new_messages}}, "$setOnInsert": {"user_id": str(current_user.id), "created_at": datetime.datetime.now(datetime.timezone.utc)}},
#         upsert=True
#     )
#     print(f"Successfully saved to conversation. ID: {convo_id_obj}")
#     return ChatResponse(response=response_text, conversation_id=str(convo_id_obj))
# import datetime
# import os
# from fastapi import APIRouter, Depends, HTTPException
# from motor.motor_asyncio import AsyncIOMotorClient
# from bson import ObjectId

# # --- LangChain Imports ---
# from langchain_core.prompts import PromptTemplate
# from langchain_core.output_parsers import StrOutputParser
# from langchain.chains import LLMChain
# from langchain_community.vectorstores.pgvector import PGVector
# from langchain_ollama import ChatOllama, OllamaEmbeddings
# from langchain_community.cross_encoders import HuggingFaceCrossEncoder
# from langchain.retrievers.document_compressors import CrossEncoderReranker
# from langchain.retrievers.contextual_compression import ContextualCompressionRetriever

# # --- Local Imports ---
# from backend.db.session import SYNC_DATABASE_URL
# from backend.schemas.chat_schema import ChatRequest, ChatResponse, TokenCounts 
# from backend.api.auth_utils import get_current_user
# from backend.models.user import User
# from backend.db.mongodb import get_mongo_db

# # --- Environment Setup & Constants ---
# router = APIRouter()
# OLLAMA_BASE_URL = os.getenv("OLLAMA_HOST", "http://ollama:11434")

# # --- Prompt Templates ---

# # This prompt is ONLY for rewriting the user's query and is always the same.
# REWRITE_PROMPT_TEMPLATE = """
# Based on the chat history below, formulate a standalone question that can be understood
# without the chat history. Do NOT answer the question, just reformulate it if needed,
# otherwise return it as is.

# Chat History:
# {chat_history}

# Latest User Question:
# {question}

# Standalone Question:
# """
# rewrite_prompt = PromptTemplate.from_template(REWRITE_PROMPT_TEMPLATE)

# # This is the default prompt for the main RAG task.
# DEFAULT_RAG_PROMPT_TEMPLATE = """
# You are an expert assistant. Use ONLY the following pieces of context to answer the user's question.
# If the answer is not in the context, just say you don't have enough information from the documents.

# CONTEXT:
# {context}

# QUESTION:
# {question}

# ANSWER:
# """
# default_rag_prompt = PromptTemplate.from_template(DEFAULT_RAG_PROMPT_TEMPLATE)

# # --- Initialize Models That Don't Change Per Request ---
# print("Initializing static models (embeddings, re-ranker)...")
# embeddings = OllamaEmbeddings(model="nomic-embed-text", base_url=OLLAMA_BASE_URL)
# cross_encoder_model = HuggingFaceCrossEncoder(model_name="cross-encoder/ms-marco-MiniLM-L-6-v2")
# output_parser = StrOutputParser()
# print("Static models initialized successfully.")


# @router.post("/chat", response_model=ChatResponse)
# async def handle_chat_request(
#     request: ChatRequest,
#     current_user: User = Depends(get_current_user),
#     mongo_db: AsyncIOMotorClient = Depends(get_mongo_db),
# ):
#     print(f"\n--- New Chat Request for user: {current_user.email} ---")
#     print(f"Original question: '{request.prompt}'")
#     model_name = request.selected_model
#     print(f"Using model: '{model_name}'")

#     # Dynamically instantiate the LLM for this specific request
#     llm = ChatOllama(
#         model=request.selected_model,
#         temperature=request.temperature,
#         top_p=request.top_p,
#         num_predict=request.max_tokens, # Ollama uses num_predict for max tokens
#         base_url=OLLAMA_BASE_URL
#     )

#     # --- 1. QUERY REWRITING STAGE ---
#     chat_history_str = ""
#     if request.conversation_id:
#         convo = await mongo_db.conversations.find_one({"_id": ObjectId(request.conversation_id), "user_id": str(current_user.id)})
#         if convo and convo.get("messages"):
#             messages = [f"{msg['role']}: {msg['message']}" for msg in convo["messages"]]
#             chat_history_str = "\n".join(messages)
            
#     # --- THIS IS THE FIX ---
#     # The rewriter chain should ALWAYS use the simple rewrite_prompt.
#     query_rewriter_chain = LLMChain(llm=llm, prompt=rewrite_prompt, output_parser=StrOutputParser())
#     response_dict = await query_rewriter_chain.ainvoke({
#         "chat_history": chat_history_str,
#         "question": request.prompt
#     })
#     rewritten_query = response_dict['text']
#     # --- END FIX ---
#     print(f"Rewritten query for retrieval: '{rewritten_query}'")

#     # --- 2. RETRIEVAL & RE-RANKING STAGE ---
#     # Determine which prompt to use for the main generation step
#     final_rag_prompt = default_rag_prompt
#     if request.custom_prompt_template:
#         print("✅ Using custom prompt template provided by user.")
#         try:
#             final_rag_prompt = PromptTemplate.from_template(request.custom_prompt_template)
#         except Exception as e:
#             print(f"⚠️ Warning: Invalid custom prompt template. Falling back to default. Error: {e}")
    
#     # (Retrieval logic is unchanged)
#     vectorstore = PGVector(connection_string=SYNC_DATABASE_URL, embedding_function=embeddings)
#     base_retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 20, "filter": {"user_id": str(current_user.id)}})
#     reranker = CrossEncoderReranker(model=cross_encoder_model, top_n=5)
#     compression_retriever = ContextualCompressionRetriever(base_compressor=reranker, base_retriever=base_retriever)
#     final_context_docs = await compression_retriever.ainvoke(rewritten_query)
#     print(f"Retrieved and re-ranked to {len(final_context_docs)} final documents.")

#     # --- 3. GENERATION STAGE ---
#     response_text = ""
#     response_metadata = {} 
#     if final_context_docs:
#         print("📚 Found relevant documents. Generating answer with RAG.")
#         context_str = "\n\n---\n\n".join([doc.page_content for doc in final_context_docs])
#         # The main RAG chain is now correctly built with the final_rag_prompt.
#         llm_response = await (final_rag_prompt | llm).ainvoke({
#             "context": context_str,
#             "question": rewritten_query
#         })
#         response_text = llm_response.content
#         response_metadata = llm_response.response_metadata
#     else:
#         print("📚 No relevant documents found. Generating answer from general knowledge.")
#         llm_response = await llm.ainvoke(rewritten_query)
#         response_text = llm_response.content
#         response_metadata = llm_response.response_metadata

#     # --- 4. PARSE TOKEN COUNTS & SAVE TO MONGODB ---
#     prompt_tokens = response_metadata.get("prompt_eval_count", 0)
#     response_tokens = response_metadata.get("eval_count", 0)
#     token_counts = TokenCounts(
#         prompt_tokens=prompt_tokens,
#         response_tokens=response_tokens,
#         total_tokens=prompt_tokens + response_tokens
#     )
#     print(f"Token Counts: {token_counts.model_dump_json()}")

#     # --- 5. SAVE TO MONGODB & RETURN RESPONSE (Unchanged) ---
#     convo_id_obj = ObjectId(request.conversation_id) if request.conversation_id else ObjectId()
#     new_messages = [{"role": "user", "message": request.prompt}, {"role": "ai", "message": response_text}]
#     await mongo_db.conversations.update_one(
#         {"_id": convo_id_obj, "user_id": str(current_user.id)},
#         {"$push": {"messages": {"$each": new_messages}}, "$setOnInsert": {"user_id": str(current_user.id), "created_at": datetime.datetime.now(datetime.timezone.utc)}},
#         upsert=True
#     )

#     print(f"Successfully saved to conversation. ID: {convo_id_obj}")
#     return ChatResponse(response=response_text, conversation_id=str(convo_id_obj),  token_counts=token_counts)
# import datetime
# import os
# from fastapi import APIRouter, Depends, HTTPException
# from motor.motor_asyncio import AsyncIOMotorClient
# from bson import ObjectId

# # --- LangChain Imports ---
# from langchain_core.prompts import PromptTemplate
# from langchain_core.output_parsers import StrOutputParser
# from langchain.chains import LLMChain
# from langchain_community.vectorstores.pgvector import PGVector
# from langchain_ollama import ChatOllama, OllamaEmbeddings
# from langchain_community.cross_encoders import HuggingFaceCrossEncoder
# from langchain.retrievers.document_compressors import CrossEncoderReranker
# from langchain.retrievers.contextual_compression import ContextualCompressionRetriever

# # --- Local Imports ---
# from backend.db.session import SYNC_DATABASE_URL
# from backend.schemas.chat_schema import ChatRequest, ChatResponse, TokenCounts 
# from backend.api.auth_utils import get_current_user
# from backend.models.user import User
# from backend.db.mongodb import get_mongo_db

# # --- Environment Setup & Constants ---
# router = APIRouter()
# OLLAMA_BASE_URL = os.getenv("OLLAMA_HOST", "http://ollama:11434")

# # --- Prompt Templates ---

# # This prompt is ONLY for rewriting the user's query and is always the same.
# TOOL_SELECTION_PROMPT_TEMPLATE = """
# You are a highly intelligent routing agent. Your job is to analyze the user's query and decide which specialized AI model is best suited to handle the request.
# You must choose from the following available models:

# - 'codellama': Best for writing, explaining, or debugging code in any language.
# - 'llama3:8b': Best for general conversation, summarization, reasoning, and answering questions based on provided text (RAG).

# Based on the user's query, you must respond with ONLY the name of the chosen model and nothing else. For example, if the query is a coding question, your entire response should be just "codellama".

# User Query:
# {question}

# Chosen Model:
# """
# tool_selection_prompt = PromptTemplate.from_template(TOOL_SELECTION_PROMPT_TEMPLATE)

# REWRITE_PROMPT_TEMPLATE = """
# Based on the chat history below, formulate a standalone question that can be understood
# without the chat history. Do NOT answer the question, just reformulate it if needed,
# otherwise return it as is.

# Chat History:
# {chat_history}

# Latest User Question:
# {question}

# Standalone Question:
# """
# rewrite_prompt = PromptTemplate.from_template(REWRITE_PROMPT_TEMPLATE)

# # This is the default prompt for the main RAG task.
# DEFAULT_RAG_PROMPT_TEMPLATE = """
# You are an expert assistant. Use ONLY the following pieces of context to answer the user's question.
# If the answer is not in the context, just say you don't have enough information from the documents.

# CONTEXT:
# {context}

# QUESTION:
# {question}

# ANSWER:
# """
# default_rag_prompt = PromptTemplate.from_template(DEFAULT_RAG_PROMPT_TEMPLATE)

# # --- Initialize Models That Don't Change Per Request ---
# print("Initializing static models (embeddings, re-ranker)...")
# embeddings = OllamaEmbeddings(model="nomic-embed-text", base_url=OLLAMA_BASE_URL)
# cross_encoder_model = HuggingFaceCrossEncoder(model_name="cross-encoder/ms-marco-MiniLM-L-6-v2")
# output_parser = StrOutputParser()
# print("Static models initialized successfully.")


# @router.post("/chat", response_model=ChatResponse)
# async def handle_chat_request(
#     request: ChatRequest,
#     current_user: User = Depends(get_current_user),
#     mongo_db: AsyncIOMotorClient = Depends(get_mongo_db),
# ):
#     print(f"\n--- New Chat Request for user: {current_user.email} ---")
#     print(f"Original question: '{request.prompt}'")

#     model_name = request.selected_model
#     print(f"Using model: '{model_name}'")

#     if model_name == "agent-mode":
#         print("Entering Agent Mode...")
#         # For routing, we use a reliable base model.
#         router_llm = ChatOllama(model="llama3:8b", temperature=0, base_url=OLLAMA_BASE_URL)
        
#         # Create a simple chain to choose the tool/model
#         model_selection_chain = tool_selection_prompt | router_llm | StrOutputParser()
        
#         chosen_model = await model_selection_chain.ainvoke({"question": request.prompt})
        
#         # Clean up the response, as LLMs can sometimes add extra text
#         chosen_model = chosen_model.strip().lower()
#         print(f"Agent has chosen model: '{chosen_model}'")

#         # --- This is the placeholder for future development ---
#         # Here, you would eventually call a function to run the chosen model,
#         # potentially with a code interpreter.
#         # For now, we will just return a message indicating the decision.
        
#         # Create a placeholder response and save it
#         response_text = f"Agent Mode: I have analyzed your request and determined the best model to use is '{chosen_model}'.\n\n(In the future, I would now proceed with executing your request using this model)."
        
#         convo_id_obj = ObjectId(request.conversation_id) if request.conversation_id else ObjectId()
#         new_messages = [{"role": "user", "message": request.prompt}, {"role": "ai", "message": response_text}]
#         await mongo_db.conversations.update_one(
#             {"_id": convo_id_obj, "user_id": str(current_user.id)},
#             {"$push": {"messages": {"$each": new_messages}}, "$setOnInsert": {"user_id": str(current_user.id), "created_at": datetime.datetime.now(datetime.timezone.utc)}},
#             upsert=True
#         )
#         # We don't have real token counts for this simulated step
#         return ChatResponse(response=response_text, conversation_id=str(convo_id_obj))

#     # Dynamically instantiate the LLM for this specific request
#     llm = ChatOllama(
#         model=request.selected_model,
#         temperature=request.temperature,
#         top_p=request.top_p,
#         num_predict=request.max_tokens, # Ollama uses num_predict for max tokens
#         base_url=OLLAMA_BASE_URL
#     )

#     # --- 1. QUERY REWRITING STAGE ---
#     chat_history_str = ""
#     if request.conversation_id:
#         convo = await mongo_db.conversations.find_one({"_id": ObjectId(request.conversation_id), "user_id": str(current_user.id)})
#         if convo and convo.get("messages"):
#             messages = [f"{msg['role']}: {msg['message']}" for msg in convo["messages"]]
#             chat_history_str = "\n".join(messages)
            
#     # --- THIS IS THE FIX ---
#     # The rewriter chain should ALWAYS use the simple rewrite_prompt.
#     query_rewriter_chain = LLMChain(llm=llm, prompt=rewrite_prompt, output_parser=StrOutputParser())
#     response_dict = await query_rewriter_chain.ainvoke({
#         "chat_history": chat_history_str,
#         "question": request.prompt
#     })
#     rewritten_query = response_dict['text']
#     # --- END FIX ---
#     print(f"Rewritten query for retrieval: '{rewritten_query}'")

#     # --- 2. RETRIEVAL & RE-RANKING STAGE ---
#     # Determine which prompt to use for the main generation step
#     final_rag_prompt = default_rag_prompt
#     if request.custom_prompt_template:
#         print("✅ Using custom prompt template provided by user.")
#         try:
#             final_rag_prompt = PromptTemplate.from_template(request.custom_prompt_template)
#         except Exception as e:
#             print(f"⚠️ Warning: Invalid custom prompt template. Falling back to default. Error: {e}")
    
#     # (Retrieval logic is unchanged)
#     vectorstore = PGVector(connection_string=SYNC_DATABASE_URL, embedding_function=embeddings)
#     base_retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 20, "filter": {"user_id": str(current_user.id)}})
#     reranker = CrossEncoderReranker(model=cross_encoder_model, top_n=5)
#     compression_retriever = ContextualCompressionRetriever(base_compressor=reranker, base_retriever=base_retriever)
#     final_context_docs = await compression_retriever.ainvoke(rewritten_query)
#     print(f"Retrieved and re-ranked to {len(final_context_docs)} final documents.")

#     # --- 3. GENERATION STAGE ---
#     response_text = ""
#     response_metadata = {} 
#     if final_context_docs:
#         print("📚 Found relevant documents. Generating answer with RAG.")
#         context_str = "\n\n---\n\n".join([doc.page_content for doc in final_context_docs])
#         # The main RAG chain is now correctly built with the final_rag_prompt.
#         llm_response = await (final_rag_prompt | llm).ainvoke({
#             "context": context_str,
#             "question": rewritten_query
#         })
#         response_text = llm_response.content
#         response_metadata = llm_response.response_metadata
#     else:
#         print("📚 No relevant documents found. Generating answer from general knowledge.")
#         llm_response = await llm.ainvoke(rewritten_query)
#         response_text = llm_response.content
#         response_metadata = llm_response.response_metadata

#     # --- 4. PARSE TOKEN COUNTS & SAVE TO MONGODB ---
#     prompt_tokens = response_metadata.get("prompt_eval_count", 0)
#     response_tokens = response_metadata.get("eval_count", 0)
#     token_counts = TokenCounts(
#         prompt_tokens=prompt_tokens,
#         response_tokens=response_tokens,
#         total_tokens=prompt_tokens + response_tokens
#     )
#     print(f"Token Counts: {token_counts.model_dump_json()}")

#     # --- 5. SAVE TO MONGODB & RETURN RESPONSE (Unchanged) ---
#     convo_id_obj = ObjectId(request.conversation_id) if request.conversation_id else ObjectId()
#     new_messages = [{"role": "user", "message": request.prompt}, {"role": "ai", "message": response_text}]
#     await mongo_db.conversations.update_one(
#         {"_id": convo_id_obj, "user_id": str(current_user.id)},
#         {"$push": {"messages": {"$each": new_messages}}, "$setOnInsert": {"user_id": str(current_user.id), "created_at": datetime.datetime.now(datetime.timezone.utc)}},
#         upsert=True
#     )

#     print(f"Successfully saved to conversation. ID: {convo_id_obj}")
#     return ChatResponse(response=response_text, conversation_id=str(convo_id_obj),  token_counts=token_counts)
import datetime
import os
from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

# LangChain Imports
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.chains import LLMChain
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

router = APIRouter()
OLLAMA_BASE_URL = os.getenv("OLLAMA_HOST", "http://ollama:11434")

# --- PROMPT TEMPLATES ---
TOOL_SELECTION_PROMPT_TEMPLATE = """
You are a highly intelligent routing agent. Your job is to analyze the user's query and decide which specialized AI model is best suited to handle the request.
You must choose from the following available models:

- 'codellama:7b': Best for writing, explaining, or debugging code in any language.
- 'llama3:8b': Best for general conversation, summarization, reasoning, and answering questions based on provided text (RAG).

Based on the user's query, you must respond with ONLY the name of the chosen model and nothing else. For example, if the query is a coding question, your entire response should be just "codellama:7b".

User Query:
{question}

Chosen Model:
"""
tool_selection_prompt = PromptTemplate.from_template(TOOL_SELECTION_PROMPT_TEMPLATE)

REWRITE_PROMPT_TEMPLATE = """
Based on the chat history below, formulate a standalone question that can be understood
without the chat history. Do NOT answer the question, just reformulate it if needed,
otherwise return it as is.

Chat History:
{chat_history}

Latest User Question:
{question}

Standalone Question:
"""
rewrite_prompt = PromptTemplate.from_template(REWRITE_PROMPT_TEMPLATE)

# This is the default prompt for the main RAG task.
DEFAULT_RAG_PROMPT_TEMPLATE = """
You are an expert assistant. Use ONLY the following pieces of context to answer the user's question.
If the answer is not in the context, just say you don't have enough information from the documents.

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
"""
default_rag_prompt = PromptTemplate.from_template(DEFAULT_RAG_PROMPT_TEMPLATE)

CODE_PROMPT_TEMPLATE = """
You are an expert programmer and master of algorithms. Provide a clear, concise, and correct code solution to the user's request.
Explain the code briefly if necessary. Use the following context if it is relevant.

CONTEXT:
{context}

REQUEST:
{question}

CODE:
"""
code_prompt = ChatPromptTemplate.from_template(CODE_PROMPT_TEMPLATE)

tool_selection_prompt = PromptTemplate.from_template(TOOL_SELECTION_PROMPT_TEMPLATE)
rewrite_prompt = PromptTemplate.from_template(REWRITE_PROMPT_TEMPLATE)
default_rag_prompt = ChatPromptTemplate.from_template(DEFAULT_RAG_PROMPT_TEMPLATE)
code_prompt = ChatPromptTemplate.from_template(CODE_PROMPT_TEMPLATE)
PROMPT_FOR_MODEL = { "codellama:7b": code_prompt, "dolphin-mistral": code_prompt }

# --- STATIC MODELS ---
print("Initializing static models (embeddings, re-ranker)...")
embeddings = OllamaEmbeddings(model="nomic-embed-text", base_url=OLLAMA_BASE_URL)
cross_encoder_model = HuggingFaceCrossEncoder(model_name="cross-encoder/ms-marco-MiniLM-L-6-v2")
output_parser = StrOutputParser()
print("Static models initialized successfully.")


# --- REUSABLE PIPELINE ---
async def run_rag_pipeline(request: ChatRequest, current_user: User, mongo_db: AsyncIOMotorClient, model_name: str) -> ChatResponse:
    print(f"--- Running RAG Pipeline with model: '{model_name}' ---")
    
    llm = ChatOllama(model=model_name, temperature=request.temperature, top_p=request.top_p, num_predict=request.max_tokens, base_url=OLLAMA_BASE_URL)

    # 1. Query Rewriting Stage
    chat_history_str = ""
    if request.conversation_id:
        convo = await mongo_db.conversations.find_one({"_id": ObjectId(request.conversation_id), "user_id": str(current_user.id)})
        if convo and convo.get("messages"):
            messages = [f"{msg['role']}: {msg['message']}" for msg in convo["messages"]]
            chat_history_str = "\n".join(messages)
    
    query_rewriter_chain = LLMChain(llm=llm, prompt=rewrite_prompt, output_parser=StrOutputParser())
    response_dict = await query_rewriter_chain.ainvoke({"chat_history": chat_history_str, "question": request.prompt})
    rewritten_query = response_dict['text']
    print(f"Rewritten query for retrieval: '{rewritten_query}'")

    # 2. Conditional Retrieval & Re-ranking Stage
    final_context_docs = []
    if request.selected_file_ids:
        print(f"✅ User has selected {len(request.selected_file_ids)} file(s). Attempting to retrieve context...")
        vectorstore = PGVector(connection_string=SYNC_DATABASE_URL, embedding_function=embeddings)
        base_retriever = vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 20, "filter": {"user_id": str(current_user.id), "file_id": {"$in": [str(fid) for fid in request.selected_file_ids]}}}
        )
        reranker = CrossEncoderReranker(model=cross_encoder_model, top_n=5)
        compression_retriever = ContextualCompressionRetriever(base_compressor=reranker, base_retriever=base_retriever)
        final_context_docs = await compression_retriever.ainvoke(rewritten_query)
    else:
        print("✅ No files selected by user. Skipping context retrieval.")
    
    # print(f"Retrieved {len(final_context_docs)} final documents for context.")

    # 3. Prompt Selection Stage
    final_rag_prompt = PROMPT_FOR_MODEL.get(model_name)
    if not final_rag_prompt:
        if request.custom_prompt_template:
            print("✅ Using custom prompt template from user.")
            try: final_rag_prompt = ChatPromptTemplate.from_template(request.custom_prompt_template)
            except Exception as e:
                print(f"⚠️ Warning: Invalid custom prompt template. Using default. Error: {e}")
                final_rag_prompt = default_rag_prompt
        else: final_rag_prompt = default_rag_prompt
    else: print(f"✅ Using specialized prompt for model '{model_name}'.")
            
    # 4. Generation Stage
    llm_response = None
    if final_context_docs:
        print("📚 Found relevant documents. Generating answer with RAG.")
        context_str = "\n\n---\n\n".join([doc.page_content for doc in final_context_docs])
        rag_chain = final_rag_prompt | llm
        llm_response = await rag_chain.ainvoke({"context": context_str, "question": rewritten_query})
    else:
        print("📚 No documents in context. Generating answer from general knowledge.")
        rag_chain = final_rag_prompt | llm
        llm_response = await rag_chain.ainvoke({"context": "", "question": rewritten_query})

    response_text = llm_response.content
    response_metadata = llm_response.response_metadata

    # 5. Parse Token Counts & Save to DB
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
    
    print(f"Successfully saved to conversation. ID: {convo_id_obj}")
    return ChatResponse(response=response_text, conversation_id=str(convo_id_obj), token_counts=token_counts)


# --- MAIN ROUTER ---
@router.post("/chat", response_model=ChatResponse)
async def handle_chat_request(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    mongo_db: AsyncIOMotorClient = Depends(get_mongo_db),
):
    print(f"\n--- New Chat Request for user: {current_user.email} ---")
    print(f"Original question: '{request.prompt}'")
    
    model_to_use = request.selected_model
    
    if model_to_use == "agent-mode":
        print("🤖 Entering Agent Mode...")
        router_llm = ChatOllama(model="llama3:8b", temperature=0, base_url=OLLAMA_BASE_URL)
        model_selection_chain = tool_selection_prompt | router_llm | StrOutputParser()
        chosen_model = await model_selection_chain.ainvoke({"question": request.prompt})
        model_to_use = chosen_model.strip().lower().split()[0]
        print(f"🤖 Agent has chosen model: '{model_to_use}'")

    return await run_rag_pipeline(request, current_user, mongo_db, model_name=model_to_use)