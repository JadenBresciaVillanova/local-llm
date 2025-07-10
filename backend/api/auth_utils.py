# backend/api/auth_utils.py

from fastapi import Depends, HTTPException, status, Request, Form, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from backend.db.session import get_db
from backend.models.user import User

# It's good practice to keep services separate, but for simplicity as requested,
# this class will remain here. It's used by both dependency functions.
class AuthService:
    """A service class to contain user-related logic."""
    @staticmethod
    async def get_or_create_user(db: AsyncSession, email: str) -> User:
        """Finds a user by email, or creates a new one if they don't exist."""
        result = await db.execute(select(User).where(User.email == email))
        user = result.scalars().first()

        if not user:
            print(f"✅ User with email '{email}' not found. Creating new user.")
            # Note: The User model has more fields now (provider, etc.)
            # This will create a user with only an email, which is fine for now
            # but will need to be updated when moving to full OAuth.
            new_user = User(email=email)
            db.add(new_user)
            await db.commit()
            await db.refresh(new_user)
            return new_user
        
        print(f"✅ Found existing user: {user.email}")
        return user

async def get_current_user_from_query(
    # This special `Query(...)` dependency tells FastAPI to look for a
    # query parameter named 'user_email' in the URL.
    user_email: str = Query(...), 
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    Gets the current user by trusting the 'user_email' query parameter.
    Used for GET requests that can't have a body.
    """
    print(f"--- Attempting to get user from query param with email: {user_email} ---")
    if not user_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User email not provided in query parameters.",
        )
    
    user = await AuthService.get_or_create_user(db, email=user_email)
    
    print(f"--- Returning user from query: {user.email} (ID: {user.id}) ---")
    return user

# --- DEPENDENCY FOR JSON REQUESTS (like /api/chat) ---

async def get_current_user(
    request: Request,
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    Gets the current user by trusting the 'user_email' field in a JSON request body.
    Used for standard API endpoints.
    """
    print("--- Attempting to get current user from JSON request body ---")
    
    # 1. Try to parse the JSON body from the request.
    try:
        body = await request.json()
    except Exception:
        print("❌ get_current_user: Could not parse JSON body from request.")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid request body. Could not parse JSON.",
        )

    # 2. Get the email from the parsed body.
    email = body.get("user_email")
    print(f"--- Extracted email from JSON body: {email} ---")

    # 3. Check if the email was found.
    if not email:
        print("❌ get_current_user: 'user_email' not found in request body.")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User email not provided in the request body.",
        )

    # 4. If we have an email, get or create the user in the database.
    user = await AuthService.get_or_create_user(db, email=email)
    
    print(f"--- Returning user from JSON: {user.email} (ID: {user.id}) ---")
    return user


# --- NEW DEPENDENCY FOR FORM-DATA REQUESTS (like /api/files/upload) ---

async def get_current_user_from_form(
    # This special `Form(...)` dependency tells FastAPI to look for a field
    # named 'user_email' inside the multipart/form-data payload.
    user_email: str = Form(...), 
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    Gets the current user by trusting the 'user_email' field in form data.
    Used for multipart/form-data requests like file uploads.
    """
    print(f"--- Attempting to get user from form data with email: {user_email} ---")
    if not user_email:
        # This check is somewhat redundant as `Form(...)` makes it required,
        # but it's good for clarity.
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User email not provided in the form data.",
        )
    
    # Reuse the same logic to find or create the user
    user = await AuthService.get_or_create_user(db, email=user_email)
    
    print(f"--- Returning user from form: {user.email} (ID: {user.id}) ---")
    return user

# from fastapi import Depends, HTTPException, status, Request
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.future import select

# # Keep all your other necessary imports like User, get_db, etc.
# from backend.db.session import get_db
# from backend.models.user import User

# class AuthService:
#     """A service class to contain user-related logic."""
#     @staticmethod
#     async def get_or_create_user(db: AsyncSession, email: str) -> User:
#         """Finds a user by email, or creates a new one if they don't exist."""
#         result = await db.execute(select(User).where(User.email == email))
#         user = result.scalars().first()

#         if not user:
#             print(f"✅ User with email '{email}' not found. Creating new user.")
#             new_user = User(email=email)
#             db.add(new_user)
#             await db.commit()
#             await db.refresh(new_user)
#             return new_user
        
#         print(f"✅ Found existing user: {user.email}")
#         return user

# # This is our temporary, insecure dependency for local development.
# # It trusts the email sent from the frontend.
# async def get_current_user(
#     request: Request,
#     db: AsyncSession = Depends(get_db)
# ) -> User:
#     """
#     Gets the current user by trusting the 'user_email' field in the request body.
#     """
#     print("--- Attempting to get current user from request body ---")
    
#     # 1. Try to parse the JSON body from the request.
#     try:
#         body = await request.json()
#     except Exception:
#         print("❌ get_current_user: Could not parse JSON body from request.")
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Invalid request body. Could not parse JSON.",
#         )

#     # 2. Get the email from the parsed body.
#     email = body.get("user_email")
#     print(f"--- Extracted email from body: {email} ---")

#     # 3. Check if the email was found.
#     if not email:
#         print("❌ get_current_user: 'user_email' not found in request body.")
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="User email not provided in the request body.",
#         )

#     # 4. If we have an email, get or create the user in the database.
#     user = await AuthService.get_or_create_user(db, email=email)
    
#     print(f"--- Returning user: {user.email} (ID: {user.id}) ---")
#     return user
    
# async def get_current_user(
#     token: str = Depends(oauth2_scheme), 
#     db: AsyncSession = Depends(get_db)
# ) -> User:
#     """
#     Dependency to get the current user.
#     1. Decodes the token from the provider (GitHub).
#     2. Gets or creates a user in our own database.
#     """
#     if not token:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Not authenticated",
#         )

#     # Decode the token to get the user's email
#     # Note: We are not verifying the signature here for simplicity.
#     claims = AuthService.decode_provider_token(token)
#     email = claims.get("email")

#     if email is None:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Could not validate credentials, email not in token.",
#         )

#     # Get the user from our database, or create them
#     user = await AuthService.get_or_create_user(db, email=email)
#     return user