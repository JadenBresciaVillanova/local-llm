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

import datetime
import asyncio
from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

# LangChain Imports
from langchain_community.vectorstores.pgvector import PGVector
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# Local Imports
from backend.db.session import SYNC_DATABASE_URL
from backend.schemas.chat_schema import ChatRequest, ChatResponse
from backend.api.auth_utils import get_current_user
from backend.models.user import User
from backend.db.mongodb import get_mongo_db

router = APIRouter()

# --- RAG Setup ---
OLLAMA_BASE_URL = "http://ollama:11434"
RAG_PROMPT_TEMPLATE = """
You are an expert assistant. Use ONLY the following pieces of context to answer the user's question.
If the answer is not in the context, just say you don't have enough information from the documents.

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
"""
rag_prompt_template = ChatPromptTemplate.from_template(RAG_PROMPT_TEMPLATE)

# 2. A general prompt for when we DON'T have context
GENERAL_PROMPT_TEMPLATE = """
You are a helpful AI assistant. Answer the user's question based on your own knowledge.

QUESTION:
{question}

ANSWER:
"""
general_prompt_template = ChatPromptTemplate.from_template(GENERAL_PROMPT_TEMPLATE)

# Initialize major components
llm = ChatOllama(model="llama3:8b", temperature=0, base_url=OLLAMA_BASE_URL)
embeddings = OllamaEmbeddings(model="nomic-embed-text", base_url=OLLAMA_BASE_URL)
# prompt_template = ChatPromptTemplate.from_template(RAG_PROMPT_TEMPLATE)
output_parser = StrOutputParser()

@router.post("/chat", response_model=ChatResponse)
async def handle_chat_request(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    mongo_db: AsyncIOMotorClient = Depends(get_mongo_db),
):
    print(f"Handling chat request for user: {current_user.email}")

    vectorstore = PGVector(
        connection_string=SYNC_DATABASE_URL,
        embedding_function=embeddings,
    )

    # --- THE FIX: Use a Stricter Retriever ---
    # We now use a different search type.
    retriever = vectorstore.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={
            "k": 3, # Still get up to 3 documents...
            "score_threshold": 0.5, # ...but ONLY if their similarity score is above this value.
            "filter": {"user_id": str(current_user.id)}
        }
    )

    # Step 1: Retrieve documents FIRST
    # The retriever will now return an empty list for "2+2" because no chunks meet the threshold.
    retrieved_docs = retriever.invoke(request.prompt)
    
    # Step 2: Check if any documents were found and format the context
    if retrieved_docs:
        print(f"📚 Found {len(retrieved_docs)} relevant document(s) above threshold. Using RAG prompt.")
        context = "\n\n---\n\n".join([doc.page_content for doc in retrieved_docs])
        prompt = rag_prompt_template.format(context=context, question=request.prompt)
    else:
        print("📚 No relevant documents found above threshold. Using general knowledge prompt.")
        prompt = general_prompt_template.format(question=request.prompt)
        
    # Step 3: Invoke the LLM with the correct prompt
    generation_chain = (llm | output_parser)
    
    print(f"Invoking LLM with final prompt...")
    response_text = generation_chain.invoke(prompt)

    # --- MongoDB Saving Logic ---
    # This logic can be simplified now that every query is a new RAG conversation.
    new_convo_doc = {
        "user_id": str(current_user.id), 
        "messages": [
            {"role": "user", "message": request.prompt},
            {"role": "ai", "message": response_text}
        ],
        "created_at": datetime.datetime.now(datetime.timezone.utc)
    }
    result = await mongo_db.conversations.insert_one(new_convo_doc)
    conversation_id_str = str(result.inserted_id)
        
    print(f"Successfully created new RAG conversation. ID: {conversation_id_str}")
    return ChatResponse(response=response_text, conversation_id=conversation_id_str)