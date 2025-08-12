# backend/services/kafka_logger.py
import json
import logging
from datetime import datetime, timezone
from typing import Dict, Any, Optional
from kafka import KafkaProducer
from dataclasses import dataclass, asdict
from enum import Enum
import uuid

logger = logging.getLogger(__name__)

class EventType(Enum):
    """Standard event types for the application"""
    FILE_UPLOADED = "file_uploaded"
    FILE_DELETED = "file_deleted"
    CHAT_STARTED = "chat_started"
    CHAT_MESSAGE_SENT = "chat_message_sent"
    CHAT_MESSAGE_RECEIVED = "chat_message_received"
    EMBEDDING_CREATED = "embedding_created"
    CHUNK_RETRIEVED = "chunk_retrieved"
    USER_LOGIN = "user_login"
    USER_LOGOUT = "user_logout"
    MODEL_INFERENCE = "model_inference"
    ERROR_OCCURRED = "error_occurred"

class KafkaTopic(Enum):
    """Kafka topics for different event categories"""
    USER_ACTIONS = "user-actions"
    SYSTEM_EVENTS = "system-events"
    CHAT_EVENTS = "chat-events"
    FILE_EVENTS = "file-events"
    ERROR_EVENTS = "error-events"

@dataclass
class StandardEvent:
    """Standardized event format for all application events"""
    event_type: str
    user_id: str
    timestamp: str
    event_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    session_id: Optional[str] = None
    
    def __post_init__(self):
        if self.event_id is None:
            self.event_id = str(uuid.uuid4())
        if self.timestamp is None:
            self.timestamp = datetime.now(timezone.utc).isoformat()

    def to_dict(self) -> Dict[str, Any]:
        """Convert event to dictionary"""
        return asdict(self)

    def to_json(self) -> str:
        """Convert event to JSON string"""
        return json.dumps(self.to_dict(), default=str)

class KafkaEventLogger:
    """Service for logging structured events to Kafka"""
    
    def __init__(
        self,
        bootstrap_servers: str = "localhost:9092",
        enabled: bool = True
    ):
        self.enabled = enabled
        self.bootstrap_servers = bootstrap_servers
        self.producer = None
        
        if self.enabled:
            try:
                self.producer = KafkaProducer(
                    bootstrap_servers=[bootstrap_servers],
                    value_serializer=lambda v: v.encode('utf-8'),
                    key_serializer=lambda k: k.encode('utf-8') if k else None,
                    retries=3,
                    acks=1
                )
                logger.info(f"Kafka producer initialized for {bootstrap_servers}")
            except Exception as e:
                logger.error(f"Failed to initialize Kafka producer: {e}")
                self.enabled = False
    
    def _send_event(self, topic: KafkaTopic, event: StandardEvent):
        """Send event to Kafka topic"""
        if not self.enabled or not self.producer:
            logger.debug(f"Kafka logging disabled, would log: {event.to_json()}")
            return
        
        try:
            future = self.producer.send(
                topic.value,
                key=event.user_id,
                value=event.to_json()
            )
            # Don't block on send, but log failures
            future.add_callback(
                lambda metadata: logger.debug(f"Event sent to {metadata.topic}")
            )
            future.add_errback(
                lambda error: logger.error(f"Failed to send event: {error}")
            )
        except Exception as e:
            logger.error(f"Error sending event to Kafka: {e}")

    def log_file_uploaded(
        self, 
        user_id: str, 
        file_name: str, 
        file_size: int,
        file_type: str,
        num_chunks: Optional[int] = None,
        processing_time_ms: Optional[int] = None,
        session_id: Optional[str] = None
    ):
        """Log file upload event"""
        metadata = {
            "file_name": file_name,
            "file_size": file_size,
            "file_type": file_type
        }
        if num_chunks is not None:
            metadata["num_chunks"] = num_chunks
        if processing_time_ms is not None:
            metadata["processing_time_ms"] = processing_time_ms
            
        event = StandardEvent(
            event_type=EventType.FILE_UPLOADED.value,
            user_id=user_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            metadata=metadata,
            session_id=session_id
        )
        self._send_event(KafkaTopic.FILE_EVENTS, event)

    def log_file_deleted(
        self,
        user_id: str,
        file_name: str,
        file_id: str,
        session_id: Optional[str] = None
    ):
        """Log file deletion event"""
        event = StandardEvent(
            event_type=EventType.FILE_DELETED.value,
            user_id=user_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            metadata={
                "file_name": file_name,
                "file_id": file_id
            },
            session_id=session_id
        )
        self._send_event(KafkaTopic.FILE_EVENTS, event)

    def log_chat_message_sent(
        self,
        user_id: str,
        message: str,
        conversation_id: str,
        model_name: Optional[str] = None,
        session_id: Optional[str] = None
    ):
        """Log chat message sent event"""
        metadata = {
            "conversation_id": conversation_id,
            "message_length": len(message),
            "has_context": bool(conversation_id)
        }
        if model_name:
            metadata["model_name"] = model_name
            
        event = StandardEvent(
            event_type=EventType.CHAT_MESSAGE_SENT.value,
            user_id=user_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            metadata=metadata,
            session_id=session_id
        )
        self._send_event(KafkaTopic.CHAT_EVENTS, event)

    def log_chat_message_received(
        self,
        user_id: str,
        response_length: int,
        conversation_id: str,
        model_name: str,
        response_time_ms: int,
        tokens_used: Optional[int] = None,
        session_id: Optional[str] = None
    ):
        """Log chat message received event"""
        metadata = {
            "conversation_id": conversation_id,
            "response_length": response_length,
            "model_name": model_name,
            "response_time_ms": response_time_ms
        }
        if tokens_used:
            metadata["tokens_used"] = tokens_used
            
        event = StandardEvent(
            event_type=EventType.CHAT_MESSAGE_RECEIVED.value,
            user_id=user_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            metadata=metadata,
            session_id=session_id
        )
        self._send_event(KafkaTopic.CHAT_EVENTS, event)

    def log_embedding_created(
        self,
        user_id: str,
        text_length: int,
        model_name: str,
        embedding_dimension: Optional[int] = None,
        processing_time_ms: Optional[int] = None,
        session_id: Optional[str] = None
    ):
        """Log embedding creation event"""
        metadata = {
            "text_length": text_length,
            "model_name": model_name
        }
        if embedding_dimension:
            metadata["embedding_dimension"] = embedding_dimension
        if processing_time_ms:
            metadata["processing_time_ms"] = processing_time_ms
            
        event = StandardEvent(
            event_type=EventType.EMBEDDING_CREATED.value,
            user_id=user_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            metadata=metadata,
            session_id=session_id
        )
        self._send_event(KafkaTopic.SYSTEM_EVENTS, event)

    def log_user_login(
        self,
        user_id: str,
        login_method: str = "oauth",
        session_id: Optional[str] = None
    ):
        """Log user login event"""
        event = StandardEvent(
            event_type=EventType.USER_LOGIN.value,
            user_id=user_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            metadata={"login_method": login_method},
            session_id=session_id
        )
        self._send_event(KafkaTopic.USER_ACTIONS, event)

    def log_error_occurred(
        self,
        user_id: str,
        error_type: str,
        error_message: str,
        endpoint: Optional[str] = None,
        stack_trace: Optional[str] = None,
        session_id: Optional[str] = None
    ):
        """Log error occurrence event"""
        metadata = {
            "error_type": error_type,
            "error_message": error_message
        }
        if endpoint:
            metadata["endpoint"] = endpoint
        if stack_trace:
            metadata["stack_trace"] = stack_trace
            
        event = StandardEvent(
            event_type=EventType.ERROR_OCCURRED.value,
            user_id=user_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            metadata=metadata,
            session_id=session_id
        )
        self._send_event(KafkaTopic.ERROR_EVENTS, event)

    def close(self):
        """Close the Kafka producer"""
        if self.producer:
            self.producer.close()

# Global instance
kafka_logger = KafkaEventLogger(enabled=False)  # Disabled by default until Kafka is set up

def get_kafka_logger() -> KafkaEventLogger:
    """Get the global Kafka logger instance"""
    return kafka_logger