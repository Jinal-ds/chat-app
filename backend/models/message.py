from beanie import Document
from pydantic import BaseModel, Field
from datetime import datetime

class Message(Document):
    room_id: str
    sender_id: str
    sender_name: str
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)  # ✅ fixed

    class Settings:
        name = "messages"

class MessageCreate(BaseModel):
    content: str

class MessageResponse(BaseModel):
    id: str
    room_id: str
    sender_name: str
    content: str
    created_at: datetime