# Standard library imports
from datetime import datetime
from typing import Optional, Dict, Any

# Third-party imports
from bson import ObjectId
from pydantic import BaseModel, Field



class Document(BaseModel):
   
    id: Optional[str] = Field(None, alias="_id")
    document_id: str = Field(..., description="Unique document identifier")
    name: str = Field(..., description="Original filename")
    topic: str = Field(..., description="Topic category")
    file_type: str = Field(..., description="File extension")
    file_size: int = Field(..., ge=0, description="File size in bytes")
    status: str = Field(default="uploaded", description="Processing status")
    chunk_count: int = Field(default=0, ge=0, description="Number of chunks")
    
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
    def from_dict(cls, data: Dict[str, Any]) -> "Document":
        if "_id" in data:
            data["_id"] = str(data["_id"])
        return cls(**data)

