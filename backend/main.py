from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import time

# Import your startup/shutdown functions and your API routers
from backend.db.mongodb import connect_to_mongo, close_mongo_connection
from backend.api import chat, conversations, users, files, metrics
from backend.services.metrics_service import MetricsService

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

# Add metrics middleware
@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    """Middleware to collect HTTP request metrics"""
    start_time = time.time()
    MetricsService.increment_active_connections()
    
    try:
        response = await call_next(request)
        
        # Record metrics
        duration = time.time() - start_time
        MetricsService.record_request_latency(
            method=request.method,
            endpoint=request.url.path,
            duration=duration
        )
        MetricsService.record_http_request(
            method=request.method,
            endpoint=request.url.path,
            status_code=response.status_code
        )
        
        return response
    except Exception as e:
        # Record error metrics
        duration = time.time() - start_time
        MetricsService.record_request_latency(
            method=request.method,
            endpoint=request.url.path,
            duration=duration
        )
        MetricsService.record_http_request(
            method=request.method,
            endpoint=request.url.path,
            status_code=500
        )
        raise
    finally:
        MetricsService.decrement_active_connections()

# 5. Include your API routers
app.include_router(chat.router, prefix="/api", tags=["Chat"])
app.include_router(users.router, prefix="/api", tags=["Users"])
app.include_router(conversations.router, prefix="/api", tags=["Conversations"])
app.include_router(files.router, prefix="/api", tags=["Files"])
app.include_router(metrics.router, tags=["Metrics"])  # Metrics at root level

# 6. Define any root-level routes
@app.get("/")
def read_root():
    return {"message": "API is running"}