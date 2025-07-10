# backend/api/users.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from backend.db.session import get_db  # <--- FIX 1: Corrected import
from backend.models.user import User
from backend.schemas.user_schema import UserCreate, UserRead

router = APIRouter()

@router.post("/auth/login", response_model=UserRead)
async def login_or_create_user(
    user_data: UserCreate, 
    db: AsyncSession = Depends(get_db)  # <--- FIX 2: Corrected dependency
):
    """
    Called by the frontend after a successful OAuth login.
    Checks if the user exists based on provider and provider_id.
    If not, creates a new user.
    Returns the user data from our database.
    (In a real app, you would also return your own JWT here).
    """
    statement = select(User).where(
        User.provider == user_data.provider, 
        User.provider_id == user_data.provider_id
    )
    result = await db.execute(statement)
    user = result.scalars().first()

    if not user:
        # User does not exist, create them
        if not user_data.email:
             raise HTTPException(status_code=400, detail="Email is required from OAuth provider")
        
        # Check if another account with this email exists
        email_statement = select(User).where(User.email == user_data.email)
        email_result = await db.execute(email_statement)
        if email_result.scalars().first():
            raise HTTPException(
                status_code=409, # Conflict
                detail=f"User with email {user_data.email} already exists but with a different login provider."
            )
            
        user = User(
            email=user_data.email,
            provider=user_data.provider,
            provider_id=user_data.provider_id
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        
    return user