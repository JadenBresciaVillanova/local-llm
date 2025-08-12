
import traceback
from sqlalchemy import select
from sqlalchemy.orm import Session

# --- LangChain Imports ---
from langchain_community.vectorstores.pgvector import PGVector
from langchain_community.document_loaders import (
    PyPDFLoader, TextLoader, UnstructuredWordDocumentLoader,
)
from langchain_ollama import OllamaEmbeddings
# NEW: Import the intelligent chunking tool
from langchain_experimental.text_splitter import SemanticChunker

# --- Local Imports ---
from backend.models.file_metadata import FileMetadata
from backend.db.session import SyncSessionLocal, SYNC_DATABASE_URL

# --- Constants ---
LOADER_MAPPING = {
    'application/pdf': PyPDFLoader,
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document': UnstructuredWordDocumentLoader,
    'text/plain': TextLoader,
}
OLLAMA_BASE_URL = "http://ollama:11434"


class ProcessingService:
    @staticmethod
    def process_file_sync(file_id: str, file_path: str, file_type: str, user_id: str):
        """
        The main processing pipeline. It loads a document, chunks it semantically,
        and stores the embeddings in the vector database.
        """
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

                # 2. Load the raw document from disk
                loader = LOADER_MAPPING.get(file_type)(file_path)
                docs = loader.load()
                # Add essential metadata to each document before splitting
                for doc in docs:
                    doc.metadata["file_id"] = file_id
                    doc.metadata["file_name"] = file_path.split('/')[-1]
                    doc.metadata["user_id"] = user_id
                
                # 3. Initialize Embedding Model (Required for the SemanticChunker)
                print("Initializing embedding model for semantic chunking...")
                embeddings = OllamaEmbeddings(model="nomic-embed-text", base_url=OLLAMA_BASE_URL)

                # 4. Split Text into Chunks using the new "intelligent" method
                text_splitter = SemanticChunker(embeddings)
                splits = text_splitter.split_documents(docs)
                chunk_count = len(splits)
                print(f"🔪 Semantically split document into {chunk_count} chunks.")

                # 5. Embed and store the chunks in PGVector
                # This reuses the embeddings model from step 3.
                # It adds all chunks to the single, shared public collection.
                print("📦 Storing chunks in vector store...")
                PGVector.from_documents(
                    documents=splits,
                    embedding=embeddings,
                    connection_string=SYNC_DATABASE_URL,
                )

                # 6. Update status to 'completed' in the database
                file_meta.processing_status = "completed"
                file_meta.chunk_count = chunk_count # Set the final chunk count
                db.commit()
                
                print(f"✅ [Sync] Successfully processed and embedded file_id: {file_id}")

            except Exception as e:
                print(f"❌❌❌ [Sync] An error occurred during file processing for {file_id}: {e}")
                traceback.print_exc()
                db.rollback()
                
                # Attempt to mark the file as 'failed' as a final step
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
                db.close() # Always ensure the session is closed.