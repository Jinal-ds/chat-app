from beanie import Document
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Room(Document):
    name: str
    description: Optional[str] = None
    created_by: str
    created_at: datetime = Field(default_factory=datetime.utcnow)  # ✅ fixed

    class Settings:
        name = "rooms"

class RoomCreate(BaseModel):
    name: str
    description: Optional[str] = None

class RoomResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    created_by: str
    created_at: datetime