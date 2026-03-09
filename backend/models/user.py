from beanie import Document
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class User(Document):
    name: str
    email: str
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)  # ✅ fixed

    class Settings:
        name = "users"

class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: str
    name: str
    email: str