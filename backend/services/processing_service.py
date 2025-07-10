# # backend/services/processing_service.py
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.future import select

# # --- LangChain Imports ---
# from langchain_community.document_loaders import (
#     PyPDFLoader,
#     TextLoader,
#     UnstructuredWordDocumentLoader,
# )
# from langchain_community.vectorstores.pgvector import PGVector                         # <-- NEW
# from langchain_ollama import OllamaEmbeddings                      # <-- NEW
# from langchain.text_splitter import RecursiveCharacterTextSplitter

# # --- Local Imports ---
# from backend.models.file_metadata import FileMetadata
# from backend.db.session import AsyncSessionLocal, DATABASE_URL

# # Define the connection string for PGVector
# # NOTE: PGVector's sync from_documents requires a sync connection string.
# # We can construct it from our async one.
# SYNC_DATABASE_URL = DATABASE_URL.replace("postgresql+asyncpg", "postgresql+psycopg2")

# # 1. Map file types to LangChain Document Loaders
# LOADER_MAPPING = {
#     'application/pdf': PyPDFLoader,
#     'application/vnd.openxmlformats-officedocument.wordprocessingml.document': UnstructuredWordDocumentLoader,
#     'text/plain': TextLoader,
# }

# class ProcessingService:
#     @staticmethod
#     def process_file_sync(file_id: str, file_path: str, file_type: str):
#         """
#         The main processing pipeline, designed to be run in a background thread.
#         LangChain's vectorstore integrations are often synchronous, making this easier.
#         """
#         print(f"🚀 [Sync] Starting background processing for file_id: {file_id}")
        
#         try:
#             # 1. Load Document
#             loader_class = LOADER_MAPPING.get(file_type)
#             if not loader_class:
#                 raise ValueError(f"Unsupported file type: {file_type}")
            
#             # For Unstructured loaders, you might need to specify mode="single" or "elements"
#             loader = loader_class(file_path)
#             docs = loader.load()
#             print(f"📄 Loaded {len(docs)} document pages/sections.")

#             # 2. Add file_id metadata to each document
#             for doc in docs:
#                 doc.metadata["file_id"] = file_id
#                 doc.metadata["file_name"] = file_path.split('/')[-1]

#             # 3. Split Text into Chunks
#             text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
#             splits = text_splitter.split_documents(docs)
#             print(f"🔪 Split document into {len(splits)} chunks.")

#             # 4. Initialize Embedding Model
#             OLLAMA_BASE_URL = "http://ollama:11434"
#             embeddings = OllamaEmbeddings(model="nomic-embed-text", base_url=OLLAMA_BASE_URL)

#             # 5. Add to Vector Store
#             # This single command handles embedding and storing the chunks.
#             # It connects to the DB, creates embeddings for each chunk, and saves them.
#             # PGVector.from_documents(
#             #     documents=splits,
#             #     embedding=embeddings,
#             #     collection_name=file_id, # Use file_id as a unique collection name
#             #     connection_string=SYNC_DATABASE_URL,
#             #     # This pre-deletes any old chunks for this file_id, making reprocessing idempotent
#             #     pre_delete_collection=True, 
#             # )
#             print(f"📦 Storing chunks in collection: {file_id}")
#             PGVector.from_documents(
#                 documents=splits,
#                 embedding=embeddings,
#                 collection_name=file_id, 
#                 connection_string=SYNC_DATABASE_URL,
#                 pre_delete_collection=True,
#             )

#             # 6. Update status in DB
#             # We still need an async session for this part.
#             async def update_status():
#                 async with AsyncSessionLocal() as db:
#                     stmt = select(FileMetadata).where(FileMetadata.id == file_id)
#                     result = await db.execute(stmt)
#                     file_meta = result.scalars().first()
#                     if file_meta:
#                         file_meta.processing_status = "completed"
#                         await db.commit()
#                         print(f"✅ [Sync] Successfully processed and embedded file_id: {file_id}")
            
#             import asyncio
#             asyncio.run(update_status())

#         except Exception as e:
#             print(f"❌❌❌ [Sync] An error occurred during file processing for {file_id}: {e}")
#             # ... (similar 'failed' status update logic as before) ...
#             import traceback
#             traceback.print_exc()
#             # ...

# backend/services/processing_service.py
import traceback
from sqlalchemy.orm import Session # Import sync Session
from sqlalchemy import select # Import sync select

# LangChain Imports
from langchain_community.vectorstores.pgvector import PGVector
from langchain_community.document_loaders import (
    PyPDFLoader, TextLoader, UnstructuredWordDocumentLoader,
)
from langchain_ollama import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Local Imports
from backend.models.file_metadata import FileMetadata
from backend.db.session import SyncSessionLocal, SYNC_DATABASE_URL

LOADER_MAPPING = {
    'application/pdf': PyPDFLoader,
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document': UnstructuredWordDocumentLoader,
    'text/plain': TextLoader,
}

OLLAMA_BASE_URL = "http://ollama:11434"

class ProcessingService:
    @staticmethod
    def process_file_sync(file_id: str, file_path: str, file_type: str,  user_id: str):
        print(f"🚀 [Sync] Starting background processing for file_id: {file_id}")
        
        # Use a `with` statement to correctly manage the session lifecycle.
        with SyncSessionLocal() as db:
            try:
                # 1. Update status to 'processing'
                stmt = select(FileMetadata).where(FileMetadata.id == file_id)
                file_meta = db.execute(stmt).scalars().first()
                if not file_meta:
                    raise ValueError(f"File {file_id} not found in database.")
                    
                file_meta.processing_status = "processing"
                db.commit()

                # 2. Load and process file
                # ... (this logic is unchanged)
                loader = LOADER_MAPPING.get(file_type)(file_path)
                docs = loader.load()
                for doc in docs:
                    doc.metadata["file_id"] = file_id
                    doc.metadata["file_name"] = file_path.split('/')[-1]
                    doc.metadata["user_id"] = user_id
                
                text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
                splits = text_splitter.split_documents(docs)
                chunk_count = len(splits)
                # 3. Embed and store in PGVector
                print(f"🔪 Split document into {chunk_count} chunks.")
                embeddings = OllamaEmbeddings(model="nomic-embed-text", base_url=OLLAMA_BASE_URL)
                PGVector.from_documents(
                    documents=splits,
                    embedding=embeddings,
                    # collection_name=file_id, 
                    connection_string=SYNC_DATABASE_URL,
                    # pre_delete_collection=True,
                )

                # 4. Update status to 'completed'
                file_meta.processing_status = "completed"
                file_meta.processing_status = "completed"
                file_meta.chunk_count = chunk_count # <-- SET THE COUNT
                db.commit()
                
                print(f"✅ [Sync] Successfully processed and embedded file_id: {file_id}")

            except Exception as e:
                print(f"❌❌❌ [Sync] An error occurred during file processing for {file_id}: {e}")
                traceback.print_exc()
                db.rollback()
                
                try:
                    stmt = select(FileMetadata).where(FileMetadata.id == file_id)
                    file_meta = db.execute(stmt).scalars().first()
                    if file_meta:
                        file_meta.processing_status = "failed"
                        db.commit()
                except Exception as final_e:
                    print(f"Could not even set status to failed: {final_e}")
                    db.rollback()

            finally:
                db.close() # Always close the session