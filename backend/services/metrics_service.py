# backend/services/metrics_service.py
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
import time
from functools import wraps
from typing import Callable, Any
import logging

# Initialize Prometheus metrics
REQUEST_COUNT = Counter(
    'http_requests_total', 
    'Total HTTP requests', 
    ['method', 'endpoint', 'status_code']
)

REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency',
    ['method', 'endpoint']
)

ACTIVE_CONNECTIONS = Gauge(
    'http_requests_in_progress',
    'Current active HTTP requests'
)

# Custom application metrics
CHAT_REQUESTS_TOTAL = Counter(
    'chat_requests_total',
    'Total chat requests processed',
    ['user_email', 'status']
)

CHAT_FAILURES_TOTAL = Counter(
    'chat_failures_total', 
    'Total chat request failures',
    ['user_email', 'error_type']
)

EMBEDDING_CREATION_TOTAL = Counter(
    'embedding_creation_total',
    'Total embeddings created',
    ['user_email', 'model_type']
)

FILE_UPLOADS_TOTAL = Counter(
    'file_uploads_total',
    'Total file uploads',
    ['user_email', 'file_type', 'status']
)

DOCUMENT_CHUNKS_CREATED_TOTAL = Counter(
    'document_chunks_created_total',
    'Total document chunks created',
    ['user_email', 'file_type']
)

LLM_RESPONSE_LATENCY = Histogram(
    'llm_response_latency_seconds',
    'LLM response time in seconds',
    ['model_name', 'user_email'],
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0, 60.0]
)

USER_ACTIVE_SESSIONS = Gauge(
    'user_active_sessions',
    'Number of active user sessions',
    ['user_email']
)

VECTOR_DB_QUERIES_TOTAL = Counter(
    'vector_db_queries_total',
    'Total vector database queries',
    ['user_email', 'query_type']
)

FILE_PROCESSING_DURATION = Histogram(
    'file_processing_duration_seconds',
    'Time taken to process uploaded files',
    ['file_type', 'processing_stage'],
    buckets=[1.0, 5.0, 10.0, 30.0, 60.0, 300.0, 600.0]
)

logger = logging.getLogger(__name__)

class MetricsService:
    """Service for recording application metrics"""

    @staticmethod
    def record_http_request(method: str, endpoint: str, status_code: int):
        """Record HTTP request metrics"""
        REQUEST_COUNT.labels(
            method=method,
            endpoint=endpoint, 
            status_code=status_code
        ).inc()

    @staticmethod
    def record_request_latency(method: str, endpoint: str, duration: float):
        """Record HTTP request latency"""
        REQUEST_LATENCY.labels(
            method=method,
            endpoint=endpoint
        ).observe(duration)

    @staticmethod
    def increment_active_connections():
        """Increment active connection counter"""
        ACTIVE_CONNECTIONS.inc()

    @staticmethod
    def decrement_active_connections():
        """Decrement active connection counter"""
        ACTIVE_CONNECTIONS.dec()

    @staticmethod
    def record_chat_request(user_email: str, status: str = "success"):
        """Record chat request metrics"""
        CHAT_REQUESTS_TOTAL.labels(
            user_email=user_email,
            status=status
        ).inc()

    @staticmethod
    def record_chat_failure(user_email: str, error_type: str):
        """Record chat failure metrics"""
        CHAT_FAILURES_TOTAL.labels(
            user_email=user_email,
            error_type=error_type
        ).inc()

    @staticmethod
    def record_embedding_creation(user_email: str, model_type: str = "default"):
        """Record embedding creation metrics"""
        EMBEDDING_CREATION_TOTAL.labels(
            user_email=user_email,
            model_type=model_type
        ).inc()

    @staticmethod
    def record_file_upload(user_email: str, file_type: str, status: str = "success"):
        """Record file upload metrics"""
        FILE_UPLOADS_TOTAL.labels(
            user_email=user_email,
            file_type=file_type,
            status=status
        ).inc()

    @staticmethod
    def record_document_chunks_created(user_email: str, file_type: str, chunk_count: int = 1):
        """Record document chunk creation metrics"""
        DOCUMENT_CHUNKS_CREATED_TOTAL.labels(
            user_email=user_email,
            file_type=file_type
        ).inc(chunk_count)

    @staticmethod
    def record_llm_response_time(model_name: str, user_email: str, duration: float):
        """Record LLM response time metrics"""
        LLM_RESPONSE_LATENCY.labels(
            model_name=model_name,
            user_email=user_email
        ).observe(duration)

    @staticmethod
    def set_user_active_session(user_email: str, active: bool):
        """Set user active session status"""
        if active:
            USER_ACTIVE_SESSIONS.labels(user_email=user_email).inc()
        else:
            USER_ACTIVE_SESSIONS.labels(user_email=user_email).dec()

    @staticmethod
    def record_vector_db_query(user_email: str, query_type: str = "similarity_search"):
        """Record vector database query metrics"""
        VECTOR_DB_QUERIES_TOTAL.labels(
            user_email=user_email,
            query_type=query_type
        ).inc()

    @staticmethod
    def record_file_processing_duration(file_type: str, processing_stage: str, duration: float):
        """Record file processing duration metrics"""
        FILE_PROCESSING_DURATION.labels(
            file_type=file_type,
            processing_stage=processing_stage
        ).observe(duration)

    @staticmethod
    def get_metrics() -> str:
        """Get metrics in Prometheus format"""
        return generate_latest()

def metrics_middleware():
    """Decorator for recording request metrics"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            MetricsService.increment_active_connections()
            
            try:
                result = await func(*args, **kwargs)
                status_code = getattr(result, 'status_code', 200)
                MetricsService.record_http_request(
                    method="POST",  # Default for API endpoints
                    endpoint=func.__name__,
                    status_code=status_code
                )
                return result
            except Exception as e:
                logger.error(f"Error in {func.__name__}: {str(e)}")
                MetricsService.record_http_request(
                    method="POST",
                    endpoint=func.__name__,
                    status_code=500
                )
                raise
            finally:
                duration = time.time() - start_time
                MetricsService.record_request_latency(
                    method="POST",
                    endpoint=func.__name__,
                    duration=duration
                )
                MetricsService.decrement_active_connections()
                
        return wrapper
    return decorator