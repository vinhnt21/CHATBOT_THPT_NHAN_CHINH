# Standard library imports
from datetime import datetime
from enum import Enum
from typing import Optional, Dict, Any

# Third-party imports
from bson import ObjectId
from pydantic import BaseModel, Field


class ErrorLevel(str, Enum):
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class ComponentType(str, Enum):
    EMBEDDING_SERVICE = "embedding_service"
    LLM_CLIENT = "llm_client"
    DOCUMENT_PROCESSOR = "document_processor"
    PINECONE_CLIENT = "pinecone_client"
    MONGODB_CLIENT = "mongodb_client"
    RAG_PIPELINE = "rag_pipeline"
    STREAMLIT_UI = "streamlit_ui"
    FILE_PROCESSOR = "file_processor"
    QUERY_ENGINE = "query_engine"


class ErrorType(str, Enum):
    API_TIMEOUT = "api_timeout"
    API_RATE_LIMIT = "api_rate_limit"
    API_AUTHENTICATION = "api_authentication"
    DATABASE_CONNECTION = "database_connection"
    FILE_PROCESSING = "file_processing"
    EMBEDDING_GENERATION = "embedding_generation"
    VECTOR_STORAGE = "vector_storage"
    QUERY_PROCESSING = "query_processing"
    VALIDATION_ERROR = "validation_error"
    UNKNOWN_ERROR = "unknown_error"


class ErrorLog(BaseModel):

    id: Optional[str] = Field(None, alias="_id")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    level: ErrorLevel = Field(..., description="Error severity level")
    component: ComponentType = Field(..., description="System component")
    topic: Optional[str] = Field(None, description="Related topic")
    error_type: ErrorType = Field(..., description="Error category")
    message: str = Field(..., description="Error message")
    details: Optional[Dict[str, Any]] = Field(default_factory=dict)
    resolved: bool = Field(default=False, description="Resolution status")
    resolution_date: Optional[datetime] = Field(None, description="Resolution timestamp")
    
    class Config:
        populate_by_name = True
        json_encoders = {
            ObjectId: str,
            datetime: lambda v: v.isoformat()
        }
        use_enum_values = True
    
    def dict(self, **kwargs) -> Dict[str, Any]:
        data = super().dict(**kwargs)
        if self.id:
            data["_id"] = ObjectId(self.id)
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ErrorLog":
        if "_id" in data:
            data["_id"] = str(data["_id"])
        return cls(**data)
    
