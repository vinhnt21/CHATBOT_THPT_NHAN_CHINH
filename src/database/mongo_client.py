# Third-party imports
from pymongo import MongoClient
from typing import Optional

# Local imports
from src.configs import mongodb_config
from src.models import ChatSession, Document, ErrorLog

client = MongoClient(mongodb_config.CONNECTION_STRING)
db = client[mongodb_config.DATABASE_NAME]

def get_collection(collection_name: str):
    return db[collection_name]


class ChatSessionCollection:
    def __init__(self):
        self.collection = get_collection(mongodb_config.CHAT_SESSION_COLLECTION)
        
    def create_session(self, session_id: str, topic: str) -> ChatSession:
        session = ChatSession(session_id=session_id, topic=topic)
        result = self.collection.insert_one(session.model_dump())
        session.id = str(result.inserted_id)
        return session
    
    def get_session(self, session_id: str) -> Optional[ChatSession]:
        session_data = self.collection.find_one({"session_id": session_id})
        if session_data:
            return ChatSession.from_dict(session_data)
        return None
    
    def update_session(self, chat_session: ChatSession) -> bool:
        """Update session with ChatSession object"""
        try:
            session_dict = chat_session.model_dump(exclude={"id"})
            result = self.collection.update_one(
                {"session_id": chat_session.session_id}, 
                {"$set": session_dict}
            )
            return result.modified_count > 0
        except Exception as e:
            print(f"Error updating session: {e}")
            return False
    
    def update_session_fields(self, session_id: str, **kwargs) -> bool:
        """Update specific fields of a session"""
        try:
            result = self.collection.update_one({"session_id": session_id}, {"$set": kwargs})
            return result.modified_count > 0
        except Exception as e:
            print(f"Error updating session fields: {e}")
            return False
    
    
class DocumentCollection:
    def __init__(self):
        self.collection = get_collection(mongodb_config.DOCUMENTS_COLLECTION)
    
    def create_document(self, document_id: str, name: str, topic: str, file_type: str, file_size: int, chunk_count: int):
        document = Document(document_id=document_id, name=name, topic=topic, file_type=file_type, file_size=file_size, chunk_count=chunk_count)
        self.collection.insert_one(document.model_dump())
        return document
    
    def get_document(self, document_id: str):
        return self.collection.find_one({"document_id": document_id})
    
    def update_document(self, document_id: str, **kwargs):
        self.collection.update_one({"document_id": document_id}, {"$set": kwargs})
    
    def get_all_documents(self):
        return list(self.collection.find())
    
class ErrorLogCollection:
    def __init__(self):
        self.collection = get_collection(mongodb_config.ERROR_LOG_COLLECTION)
        
    def create_error_log(self, error_id: str, message: str, level: str, component: str, topic: str):
        error_log = ErrorLog(error_id=error_id, message=message, level=level, component=component, topic=topic)
        self.collection.insert_one(error_log.model_dump())
        return error_log
    
    def get_all_error_logs(self):
        return list(self.collection.find())
    
    def get_error_log(self, error_id: str):
        return self.collection.find_one({"error_id": error_id})
    

chat_session_collection = ChatSessionCollection()
document_collection = DocumentCollection()
error_log_collection = ErrorLogCollection()

__all__ = ["chat_session_collection", "document_collection", "error_log_collection"]