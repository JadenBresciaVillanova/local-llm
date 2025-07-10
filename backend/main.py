from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

# Import your startup/shutdown functions and your API routers
from backend.db.mongodb import connect_to_mongo, close_mongo_connection
from backend.api import chat, conversations, users, files

# 1. Define the lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handles application startup and shutdown events."""
    print("API starting up...")
    await connect_to_mongo()
    yield
    print("API shutting down...")
    await close_mongo_connection()

# 2. Create the FastAPI app instance, passing the lifespan manager
app = FastAPI(lifespan=lifespan, title="Local RAG API")

# 3. Define the allowed origins for CORS
origins = [
    "http://localhost",
    "http://localhost:3000",
]

# 4. Add the CORS middleware to the app
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 5. Include your API routers
# app.include_router(chat.router, prefix="/api")

# 5. Include your API routers
app.include_router(chat.router, prefix="/api", tags=["Chat"])
app.include_router(users.router, prefix="/api", tags=["Users"]) # Assuming you will use this
# 👇 ADD THE NEW ROUTER
app.include_router(conversations.router, prefix="/api", tags=["Conversations"])
app.include_router(files.router, prefix="/api", tags=["Files"]) # Add the new router

# 6. Define any root-level routes
@app.get("/")
def read_root():
    return {"message": "API is running"}