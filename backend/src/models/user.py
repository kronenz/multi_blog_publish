from pydantic import BaseModel, EmailStr, Field
from uuid import UUID, uuid4
from datetime import datetime

class User(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    email: EmailStr
    password_hash: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
