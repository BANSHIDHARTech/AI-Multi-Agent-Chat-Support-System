from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class MessageBase(BaseModel):
    content: str = Field(..., min_length=1)

class MessageCreate(MessageBase):
    conversation_id: Optional[int] = None

class MessageResponse(MessageBase):
    id: int
    conversation_id: int
    timestamp: datetime
    is_user: bool
    
    class Config:
        from_attributes = True

class ConversationResponse(BaseModel):
    id: int
    messages: List[MessageResponse]
    created_at: datetime
    
    class Config:
        from_attributes = True
