# backend/api/utils.py
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from backend.db.session import get_db
from backend.models.user import User

async def get_current_user(db: AsyncSession = Depends(get_db)) -> User:
    """
    This is a DUMMY dependency for development.
    It just returns the first user in the database.
    REPLACE THIS with real JWT token validation.
    """
    result = await db.execute(select(User))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="No users found. Please log in first.")
    return user