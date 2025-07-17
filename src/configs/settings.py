"""
Settings Configuration for THCS Nhân Chính Chatbot
Contains all application settings, API configurations, and environment management.
"""

# Standard library imports
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List

# Third-party imports
import streamlit as st

@dataclass
class AppConfig:
    """Main application configuration"""
    
    APP_NAME: str = "Chatbot THCS Nhân Chính"
    VERSION: str = "0.0.1"
    
    # File Upload Limits
    MAX_UPLOAD_SIZE_MB: int = int(st.secrets.get("MAX_UPLOAD_SIZE_MB", 10))
    ALLOWED_FILE_TYPES: List[str] = field(default_factory=lambda: [".pdf", ".docx", ".txt", ".md"])
    
    # Topics Configuration
    SUPPORTED_TOPICS: Dict[str, Dict] = field(default_factory=lambda: {
        "thong_tin_truong": {
            "display_name": "Thông tin trường",
            "description": "Lịch sử, cơ sở vật chất, quy chế, hoạt động ngoại khóa",
        }
    })


@dataclass
class DeepSeekConfig:
    """DeepSeek API configuration"""
    
    API_KEY: str = st.secrets.get("DEEPSEEK_API_KEY", "")
    BASE_URL: str = st.secrets.get("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
    MODEL: str = st.secrets.get("DEEPSEEK_MODEL", "deepseek-chat")
    TEMPERATURE: float = float(st.secrets.get("DEEPSEEK_TEMPERATURE", 0.1))


@dataclass 
class OpenAIConfig:
    """OpenAI API configuration (for embeddings)"""
    
    API_KEY: str = st.secrets.get("OPENAI_API_KEY", "")
    BASE_URL: str = st.secrets.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
    EMBEDDING_MODEL: str = st.secrets.get("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
    LLM_MODEL: str = st.secrets.get("OPENAI_LLM_MODEL", "gpt-4o-mini")
    TEMPERATURE: float = float(st.secrets.get("OPENAI_TEMPERATURE", 0.1))


@dataclass
class PineconeConfig:
    """Pinecone vector database configuration"""
    class NAME_SPACE(Enum):
        THONG_TIN_TRUONG = "thong_tin_truong"
        THONG_TIN_LOP = "thong_tin_lop"
        THONG_TIN_GIAO_VIEN = "thong_tin_giao_vien"
        THONG_TIN_SINH_VIEN = "thong_tin_sinh_vien"
        THONG_TIN_PHU_HUYNH = "thong_tin_phu_huynh"
        
    API_KEY: str = st.secrets.get("PINECONE_API_KEY", "")
    INDEX_NAME: str = st.secrets.get("PINECONE_INDEX_NAME", "thpt-nhan-chinh-kb")
    DIMENSION: int = int(st.secrets.get("PINECONE_DIMENSION", 1536))
    TOP_K: int = int(st.secrets.get("PINECONE_TOP_K", 7))


@dataclass
class MongoDBConfig:
    """MongoDB configuration"""
    
    CONNECTION_STRING: str = st.secrets.get("MONGODB_CONNECTION_STRING", "")
    DATABASE_NAME: str = st.secrets.get("MONGODB_DATABASE_NAME", "chatbot_thcs_nhan_chinh")
    CHAT_SESSION_COLLECTION: str = st.secrets.get("MONGODB_CHAT_SESSION_COLLECTION", "chat_sessions")
    DOCUMENTS_COLLECTION: str = st.secrets.get("MONGODB_DOCUMENTS_COLLECTION", "documents")
    ERROR_LOG_COLLECTION: str = st.secrets.get("MONGODB_ERROR_LOG_COLLECTION", "error_logs")

@dataclass 
class RAGConfig:
    """RAG (Retrieval Augmented Generation) configuration"""
    
    CHUNK_SIZE: int = int(st.secrets.get("RAG_CHUNK_SIZE", 1024))
    CHUNK_OVERLAP: int = int(st.secrets.get("RAG_CHUNK_OVERLAP", 128))
    SIMILARITY_TOP_K: int = int(st.secrets.get("RAG_SIMILARITY_TOP_K", 7))


# Export configuration instances
app_config = AppConfig()
deepseek_config = DeepSeekConfig()
openai_config = OpenAIConfig()
pinecone_config = PineconeConfig()
mongodb_config = MongoDBConfig()
rag_config = RAGConfig()

# Export all
__all__ = [
    "app_config",
    "deepseek_config", 
    "openai_config",
    "pinecone_config",
    "mongodb_config",
    "rag_config",
] 