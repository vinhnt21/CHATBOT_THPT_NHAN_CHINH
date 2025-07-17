# Standard library imports
from datetime import datetime
from typing import Optional, Dict, Any, List

# Third-party imports
from bson import ObjectId
from pydantic import BaseModel, Field


class Message(BaseModel):
    role: str = Field(..., description="User or System")
    content: str = Field(..., description="Content")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class ChatSession(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    session_id: str = Field(..., description="Session identifier")
    topic: str = Field(..., description="Session topic")
    start_time: datetime = Field(default_factory=datetime.utcnow)
    messages: List[Message] = Field(default_factory=list, description="Messages history")
    
    class Config:
        populate_by_name = True
        json_encoders = {
            ObjectId: str,
            datetime: lambda v: v.isoformat()
        }
    
    def dict(self, **kwargs) -> Dict[str, Any]:
        data = super().dict(**kwargs)
        if self.id:
            data["_id"] = ObjectId(self.id)
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ChatSession":
        if "_id" in data:
            data["_id"] = str(data["_id"])
        return cls(**data)
    
    def add_query(
        self,
        query: str,
        response: str,
        sources: Optional[List[str]] = None,
    ) -> None:
        query_record = QueryRecord(
            query=query,
            response=response,
            sources=sources or [],
        )
        
        self.queries.append(query_record)
        self.query_count = len(self.queries)
    
    
    
