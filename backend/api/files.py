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
    Query,
)

from fastapi.concurrency import run_in_threadpool
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func  

# LangChain Import
from langchain_community.vectorstores.pgvector import PGVector

# Local Application Imports
from backend.db.session import get_db, SYNC_DATABASE_URL
from backend.models.user import User
from backend.models.file_metadata import FileMetadata
from backend.services.file_service import FileService
from backend.services.processing_service import ProcessingService
from backend.api.auth_utils import get_current_user_from_query, get_current_user_from_form
from backend.schemas.file_schema import FileMetadataRead

router = APIRouter()

@router.post("/files/upload", response_model=FileMetadataRead)
async def upload_file(
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
        initial_metadata = await FileService.save_file(
            db=db, user=current_user, file=file
        )
        file_id = initial_metadata.id
        
        print(f"File saved. Starting sequential processing for {file_id}...")
        
        await run_in_threadpool(
            ProcessingService.process_file_sync, 
            file_id=str(file_id),
            file_path=initial_metadata.file_path,
            file_type=initial_metadata.file_type,
            user_id=str(current_user.id)
        )
        
        print(f"Sequential processing finished for {file_id}.")

        stmt = select(FileMetadata).where(FileMetadata.id == file_id)
        result = await db.execute(stmt)
        updated_metadata = result.scalars().first()
        
        if not updated_metadata:
            raise HTTPException(status_code=404, detail="Could not find file metadata after processing.")

        response_data = FileMetadataRead.model_validate(updated_metadata)
        return response_data

    except Exception as e:
        print(f"Error during file upload: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="An error occurred during file upload.")

@router.get("/files/active", response_model=List[FileMetadataRead])
async def get_active_files(
    current_user: User = Depends(get_current_user_from_query),
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieves a list of the LATEST version of each unique file for the user
    that is fully processed and physically exists on disk.
    """
    
    # 1. Create a subquery to find the latest upload_date for each file_name
    #    for the current user.
    subquery = (
        select(
            FileMetadata.file_name,
            func.max(FileMetadata.upload_date).label("max_upload_date")
        )
        .where(FileMetadata.user_id == current_user.id)
        .group_by(FileMetadata.file_name)
        .subquery()
    )
    
    # 2. Join the FileMetadata table with the subquery result.
    stmt = (
        select(FileMetadata)
        .join(
            subquery,
            (FileMetadata.file_name == subquery.c.file_name) &
            (FileMetadata.upload_date == subquery.c.max_upload_date)
        )
        .where(FileMetadata.user_id == current_user.id)
        .where(FileMetadata.processing_status == "completed")
        .order_by(FileMetadata.upload_date.desc())
    )

    result = await db.execute(stmt)
    all_latest_files = result.scalars().all()

    # Filter for files that physically exist on disk
    active_files = [f for f in all_latest_files if os.path.exists(f.file_path)]
    
    return active_files


@router.get("/files/history", response_model=List[FileMetadataRead])
async def get_upload_history(
    current_user: User = Depends(get_current_user_from_query),
    db: AsyncSession = Depends(get_db),
    limit: int = Query(5, ge=1, le=100)
):
    """
    Retrieves a paginated history of all file upload records for the user.
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

    if not file_to_delete or file_to_delete.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="File not found or permission denied.")

    # Delete from Vector Store (if applicable)
    try:
        vectorstore = PGVector(
            connection_string=SYNC_DATABASE_URL,
            embedding_function=None,
            collection_name=str(file_id),
        )
        vectorstore.delete_collection()
        print(f"🗑️ Deleted collection '{file_id}' from PGVector.")
    except Exception as e:
        print(f"⚠️ Could not delete PGVector collection '{file_id}': {e}")

    # Delete file from disk
    try:
        if os.path.exists(file_to_delete.file_path):
            os.remove(file_to_delete.file_path)
            print(f"🗑️ Deleted file from disk: {file_to_delete.file_path}")
        else:
            print(f"File not found on disk, skipping deletion: {file_to_delete.file_path}")
    except OSError as e:
        print(f"⚠️ Could not delete file from disk '{file_to_delete.file_path}': {e}")
    
    # Delete metadata from DB
    await db.delete(file_to_delete)
    await db.commit()

    return None