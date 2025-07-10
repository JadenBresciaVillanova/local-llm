# # backend/api/files.py
# # backend/api/files.py
# from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
# from sqlalchemy.ext.asyncio import AsyncSession
# # No longer need UUID here as Pydantic will handle it
# # from uuid import UUID 

# from backend.db.session import get_db
# from backend.models.user import User
# from backend.services.file_service import FileService
# from backend.api.auth_utils import get_current_user_from_form
# from backend.schemas.file_schema import FileMetadataRead

# router = APIRouter()

# @router.post("/files/upload", response_model=FileMetadataRead)
# async def upload_file(
#     db: AsyncSession = Depends(get_db),
#     file: UploadFile = File(...),
#     current_user: User = Depends(get_current_user_from_form),
# ):
#     """
#     Handles file upload, saves it, and creates a metadata record.
#     """
#     if not file.filename:
#         raise HTTPException(status_code=400, detail="No file name provided.")
        
#     try:
#         committed_metadata_orm = await FileService.save_file(
#             db=db, user=current_user, file=file
#         )
        
#         # Use model_validate instead of from_orm
#         response_data = FileMetadataRead.model_validate(committed_metadata_orm)
#         return response_data

#     except Exception as e:
#         import traceback
#         print(f"❌ Error during file upload: {e}")
#         traceback.print_exc()
#         raise HTTPException(status_code=500, detail=f"An error occurred during file upload.")

# We need a new schema to represent the response
# Create/update backend/schemas/file_schema.py

# backend/api/files.py
# from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, BackgroundTasks # Add BackgroundTasks
# from sqlalchemy.ext.asyncio import AsyncSession
# from backend.db.session import get_db
# from backend.models.user import User
# from backend.schemas.file_schema import FileMetadataRead
# from backend.services.file_service import FileService
# from backend.services.processing_service import ProcessingService # Import the new service

# # backend/api/files.py
# import os # <-- Add os import
# from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, BackgroundTasks
# from sqlalchemy.future import select
# from typing import List # <-- Add List import
# # LangChain Import
# from langchain_community.vectorstores.pgvector import PGVector
# # ... other local imports
# from backend.db.session import get_db, SYNC_DATABASE_URL
# from backend.models.file_metadata import FileMetadata
# from backend.api.auth_utils import get_current_user, get_current_user_from_query, get_current_user_from_form

# # ... router setup
# router = APIRouter()


# @router.post("/files/upload", response_model=FileMetadataRead)
# async def upload_file(
#     background_tasks: BackgroundTasks, # Inject BackgroundTasks
#     db: AsyncSession = Depends(get_db),
#     file: UploadFile = File(...),
#     current_user: User = Depends(get_current_user_from_form),
# ):
#     """
#     Handles file upload, saves it, and triggers background processing.
#     """
#     if not file.filename:
#         raise HTTPException(status_code=400, detail="No file name provided.")
        
#     try:
#         committed_metadata_orm = await FileService.save_file(
#             db=db, user=current_user, file=file
#         )
        
#         # --- TRIGGER BACKGROUND TASK ---
#         # The response is sent to the user immediately, and this runs in the background.
#         background_tasks.add_task(
#             ProcessingService.process_file_sync, 
#             str(committed_metadata_orm.id),  # Pass ID, path, and type as simple strings
#             committed_metadata_orm.file_path,
#             committed_metadata_orm.file_type,
#         )
        
#         response_data = FileMetadataRead.model_validate(committed_metadata_orm)
#         return response_data

#     except Exception as e:
#         import traceback
#         print(f"❌ Error during file upload: {e}")
#         traceback.print_exc()
#         raise HTTPException(status_code=500, detail=f"An error occurred during file upload.")
# # --- GET /files ---
# @router.get("/files", response_model=List[FileMetadataRead])
# async def get_uploaded_files(
#     # Use the new dependency that reads from query parameters
#     current_user: User = Depends(get_current_user_from_query), 
#     db: AsyncSession = Depends(get_db)
# ):
#     # ... (the rest of the function is the same)
#     stmt = (
#         select(FileMetadata)
#         .where(FileMetadata.user_id == current_user.id)
#         .order_by(FileMetadata.upload_date.desc())
#     )
#     result = await db.execute(stmt)
#     files = result.scalars().all()
#     return files

# # --- DELETE /files/{file_id} ---
# @router.delete("/files/{file_id}", status_code=204)
# async def delete_file(
#     file_id: str,
#     # Also use the new dependency here
#     current_user: User = Depends(get_current_user_from_query),
#     db: AsyncSession = Depends(get_db)
# ):
#     """
#     Deletes a file, its chunks from the vector store, and its metadata.
#     """
#     stmt = select(FileMetadata).where(FileMetadata.id == file_id)
#     result = await db.execute(stmt)
#     file_to_delete = result.scalars().first()

#     # Security Check
#     if not file_to_delete or file_to_delete.user_id != current_user.id:
#         raise HTTPException(status_code=404, detail="File not found or permission denied.")

#     # 1. Delete from Vector Store
#     try:
#         vectorstore = PGVector(
#             connection_string=SYNC_DATABASE_URL,
#             embedding_function=None, # Not needed for deletion
#             collection_name=file_id,
#         )
#         vectorstore.delete_collection()
#         print(f"🗑️ Deleted collection '{file_id}' from PGVector.")
#     except Exception as e:
#         # It's okay if the collection doesn't exist, log it and continue
#         print(f"⚠️ Could not delete PGVector collection '{file_id}': {e}")

#     # 2. Delete file from disk
#     try:
#         os.remove(file_to_delete.file_path)
#         print(f"🗑️ Deleted file from disk: {file_to_delete.file_path}")
#     except OSError as e:
#         print(f"⚠️ Could not delete file from disk '{file_to_delete.file_path}': {e}")
    
#     # 3. Delete metadata from DB
#     await db.delete(file_to_delete)
#     await db.commit()

#     return None # Return 204 No Content

# backend/api/files.py
# import os
# import traceback
# from typing import List
# from uuid import UUID

# from fastapi import (
#     APIRouter,
#     Depends,
#     UploadFile,
#     File,
#     HTTPException,
#     BackgroundTasks,
#     Query,
# )
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.future import select

# # LangChain Import for deletion logic
# from langchain_community.vectorstores.pgvector import PGVector

# # Local Application Imports
# from backend.db.session import get_db, SYNC_DATABASE_URL
# from backend.models.user import User
# from backend.models.file_metadata import FileMetadata
# from backend.services.file_service import FileService
# from backend.services.processing_service import ProcessingService
# from backend.api.auth_utils import get_current_user_from_query, get_current_user_from_form
# from backend.schemas.file_schema import FileMetadataRead

# router = APIRouter()

# @router.post("/files/upload", response_model=FileMetadataRead)
# async def upload_file(
#     background_tasks: BackgroundTasks,
#     db: AsyncSession = Depends(get_db),
#     file: UploadFile = File(...),
#     current_user: User = Depends(get_current_user_from_form),
# ):
#     """
#     Handles file upload, saves it, and triggers background processing.
#     """
#     if not file.filename:
#         raise HTTPException(status_code=400, detail="No file name provided.")
        
#     try:
#         # Save the initial file and metadata record
#         metadata_orm = await FileService.save_file(
#             db=db, user=current_user, file=file
#         )
        
#         # Trigger the background task to parse, chunk, and embed the file
#         background_tasks.add_task(
#             ProcessingService.process_file_sync, 
#             str(metadata_orm.id),
#             metadata_orm.file_path,
#             metadata_orm.file_type,
#             str(current_user.id)
#         )
        
#         # Return the initial metadata to the client immediately
#         response_data = FileMetadataRead.model_validate(metadata_orm)
#         return response_data

#     except Exception as e:
#         print(f"❌ Error during file upload: {e}")
#         traceback.print_exc()
#         raise HTTPException(status_code=500, detail="An error occurred during file upload.")

# @router.get("/files/active", response_model=List[FileMetadataRead])
# async def get_active_files(
#     current_user: User = Depends(get_current_user_from_query),
#     db: AsyncSession = Depends(get_db)
# ):
#     """
#     Retrieves a list of all files for the user that are fully processed
#     and physically exist on disk, representing the current active set.
#     """
#     # Get all file metadata from the DB for the user with 'completed' status
#     stmt = (
#         select(FileMetadata)
#         .where(FileMetadata.user_id == current_user.id)
#         .where(FileMetadata.processing_status == "completed")
#     )
#     result = await db.execute(stmt)
#     all_completed_files = result.scalars().all()

#     # Filter the list to only include files that still exist on the filesystem
#     active_files = [f for f in all_completed_files if os.path.exists(f.file_path)]
    
#     # Sort by upload date descending
#     active_files.sort(key=lambda x: x.upload_date, reverse=True)
    
#     return active_files

# @router.get("/files/history", response_model=List[FileMetadataRead])
# async def get_upload_history(
#     current_user: User = Depends(get_current_user_from_query),
#     db: AsyncSession = Depends(get_db),
#     limit: int = Query(5, ge=1, le=100)
# ):
#     """
#     Retrieves a paginated history of all file upload records for the user,
#     ordered by most recent.
#     """
#     stmt = (
#         select(FileMetadata)
#         .where(FileMetadata.user_id == current_user.id)
#         .order_by(FileMetadata.upload_date.desc())
#         .limit(limit)
#     )
#     result = await db.execute(stmt)
#     files = result.scalars().all()
#     return files

# @router.delete("/files/{file_id}", status_code=204)
# async def delete_file(
#     file_id: UUID,
#     current_user: User = Depends(get_current_user_from_query),
#     db: AsyncSession = Depends(get_db)
# ):
#     """
#     Deletes a file, its chunks from the vector store, and its metadata.
#     """
#     stmt = select(FileMetadata).where(FileMetadata.id == file_id)
#     result = await db.execute(stmt)
#     file_to_delete = result.scalars().first()

#     # Security Check
#     if not file_to_delete or file_to_delete.user_id != current_user.id:
#         raise HTTPException(status_code=404, detail="File not found or permission denied.")

#     # 1. Delete from Vector Store collection
#     try:
#         vectorstore = PGVector(
#             connection_string=SYNC_DATABASE_URL,
#             embedding_function=None, # Not needed for deletion
#             collection_name=str(file_id),
#         )
#         vectorstore.delete_collection()
#         print(f"🗑️ Deleted collection '{file_id}' from PGVector.")
#     except Exception as e:
#         # It's okay if the collection doesn't exist, log it and continue
#         print(f"⚠️ Could not delete PGVector collection '{file_id}': {e}")

#     # 2. Delete file from disk
#     try:
#         if os.path.exists(file_to_delete.file_path):
#             os.remove(file_to_delete.file_path)
#             print(f"🗑️ Deleted file from disk: {file_to_delete.file_path}")
#         else:
#             print(f"File not found on disk, skipping deletion: {file_to_delete.file_path}")
#     except OSError as e:
#         print(f"⚠️ Could not delete file from disk '{file_to_delete.file_path}': {e}")
    
#     # 3. Delete metadata from DB
#     await db.delete(file_to_delete)
#     await db.commit()

#     return None # Return 204 No Content
import os
import traceback
from typing import List
from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    UploadFile,
    File,
    HTTPException,
    BackgroundTasks,
    Query,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

# LangChain Import for deletion logic
from langchain_community.vectorstores.pgvector import PGVector

# Local Application Imports
from backend.db.session import get_db, SYNC_DATABASE_URL
from backend.models.user import User
from backend.models.file_metadata import FileMetadata
from backend.services.file_service import FileService
from backend.services.processing_service import ProcessingService
from backend.api.auth_utils import get_current_user_from_query, get_current_user_from_form
from backend.schemas.file_schema import FileMetadataRead
from fastapi.concurrency import run_in_threadpool

router = APIRouter()

@router.post("/files/upload", response_model=FileMetadataRead)
async def upload_file(
    # NOTE: We removed BackgroundTasks from the signature
    db: AsyncSession = Depends(get_db),
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user_from_form),
):
    """
    Handles file upload, saves it, and COMPLETES processing before responding.
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file name provided.")
        
    try:
        # Step 1: Save the initial file and metadata record
        initial_metadata = await FileService.save_file(
            db=db, user=current_user, file=file
        )
        file_id = initial_metadata.id # Capture the ID to use later
        
        print(f"File saved. Starting sequential processing for {file_id}...")
        
        # Step 2: Run the synchronous processing task in a threadpool
        await run_in_threadpool(
            ProcessingService.process_file_sync, 
            file_id=str(file_id),
            file_path=initial_metadata.file_path,
            file_type=initial_metadata.file_type,
            user_id=str(current_user.id)
        )
        
        print(f"Sequential processing finished for {file_id}.")

        # --- THE FIX ---
        # Step 3: Re-fetch the object from the database using the original async session.
        # This gives us a "clean" object with all the updated fields.
        stmt = select(FileMetadata).where(FileMetadata.id == file_id)
        result = await db.execute(stmt)
        updated_metadata = result.scalars().first()
        
        # If for some reason it's not found, handle it.
        if not updated_metadata:
            raise HTTPException(status_code=404, detail="Could not find file metadata after processing.")

        # Step 4: Convert the clean, updated object to our Pydantic response model.
        response_data = FileMetadataRead.model_validate(updated_metadata)
        return response_data

    except Exception as e:
        print(f"❌ Error during file upload: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="An error occurred during file upload.")

@router.get("/files/active", response_model=List[FileMetadataRead])
async def get_active_files(
    current_user: User = Depends(get_current_user_from_query),
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieves a list of all files for the user that are fully processed
    and physically exist on disk, representing the current active set.
    """
    # Get all file metadata from the DB for the user with 'completed' status
    stmt = (
        select(FileMetadata)
        .where(FileMetadata.user_id == current_user.id)
        .where(FileMetadata.processing_status == "completed")
    )
    result = await db.execute(stmt)
    all_completed_files = result.scalars().all()

    # Filter the list to only include files that still exist on the filesystem
    active_files = [f for f in all_completed_files if os.path.exists(f.file_path)]
    
    # Sort by upload date descending
    active_files.sort(key=lambda x: x.upload_date, reverse=True)
    
    return active_files

@router.get("/files/history", response_model=List[FileMetadataRead])
async def get_upload_history(
    current_user: User = Depends(get_current_user_from_query),
    db: AsyncSession = Depends(get_db),
    limit: int = Query(5, ge=1, le=100)
):
    """
    Retrieves a paginated history of all file upload records for the user,
    ordered by most recent.
    """
    stmt = (
        select(FileMetadata)
        .where(FileMetadata.user_id == current_user.id)
        .order_by(FileMetadata.upload_date.desc())
        .limit(limit)
    )
    result = await db.execute(stmt)
    files = result.scalars().all()
    return files

@router.delete("/files/{file_id}", status_code=204)
async def delete_file(
    file_id: UUID,
    current_user: User = Depends(get_current_user_from_query),
    db: AsyncSession = Depends(get_db)
):
    """
    Deletes a file, its chunks from the vector store, and its metadata.
    """
    stmt = select(FileMetadata).where(FileMetadata.id == file_id)
    result = await db.execute(stmt)
    file_to_delete = result.scalars().first()

    # Security Check
    if not file_to_delete or file_to_delete.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="File not found or permission denied.")

    # 1. Delete from Vector Store collection
    try:
        vectorstore = PGVector(
            connection_string=SYNC_DATABASE_URL,
            embedding_function=None, # Not needed for deletion
            collection_name=str(file_id),
        )
        vectorstore.delete_collection()
        print(f"🗑️ Deleted collection '{file_id}' from PGVector.")
    except Exception as e:
        # It's okay if the collection doesn't exist, log it and continue
        print(f"⚠️ Could not delete PGVector collection '{file_id}': {e}")

    # 2. Delete file from disk
    try:
        if os.path.exists(file_to_delete.file_path):
            os.remove(file_to_delete.file_path)
            print(f"🗑️ Deleted file from disk: {file_to_delete.file_path}")
        else:
            print(f"File not found on disk, skipping deletion: {file_to_delete.file_path}")
    except OSError as e:
        print(f"⚠️ Could not delete file from disk '{file_to_delete.file_path}': {e}")
    
    # 3. Delete metadata from DB
    await db.delete(file_to_delete)
    await db.commit()

    return None # Return 204 No Content