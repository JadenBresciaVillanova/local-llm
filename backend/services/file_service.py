# backend/services/file_service.py
import os
from pathlib import Path
from uuid import uuid4, UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload # Import selectinload
from fastapi import UploadFile

from backend.models.user import User
from backend.models.file_metadata import FileMetadata

UPLOAD_DIR = Path(__file__).parent.parent.resolve() / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

class FileService:
    @staticmethod
    async def save_file(
        db: AsyncSession,
        user: User,
        file: UploadFile,
    ) -> FileMetadata:
        """
        Saves an uploaded file to the disk and creates a metadata record in the DB.
        """
        # ... (save file to disk logic) ...
        file_path = UPLOAD_DIR / file.filename
        try:
            with open(file_path, "wb") as buffer:
                content = await file.read()
                buffer.write(content)
        except Exception as e:
            print(f"Error saving file to disk: {e}")
            raise

        file_size = file_path.stat().st_size
        
        # --- NEW STRATEGY ---
        
        # 1. Generate ID, create object, add, and commit.
        new_id: UUID = uuid4()
        new_metadata = FileMetadata(
            id=new_id,
            user_id=user.id,
            file_name=file.filename,
            file_path=str(file_path),
            file_size=file_size,
            file_type=file.content_type,
            processing_status="uploaded"
        )
        db.add(new_metadata)
        await db.commit()

        # 2. Select the object again, but this time, explicitly "eager load"
        #    the 'user' relationship so SQLAlchemy doesn't try to lazy-load it later.
        stmt = (
            select(FileMetadata)
            .where(FileMetadata.id == new_id)
            .options(selectinload(FileMetadata.user)) # Eagerly load the user
        )
        result = await db.execute(stmt)
        committed_metadata = result.scalars().one()

        # 3. Access the attributes we need for the print statement.
        #    This will now work because the user object was loaded with the metadata.
        print(f"✅ Successfully saved file '{committed_metadata.file_name}' for user {committed_metadata.user.email}")
        print(f"   - DB Record ID: {committed_metadata.id}")
        
        # 4. Detach the object from the session. This turns it into a plain
        #    object with no ability to perform further database operations.
        #    This is a final guarantee against any lazy-loading.
        db.expunge(committed_metadata)
        
        return committed_metadata