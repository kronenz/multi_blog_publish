from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
import uuid

class User(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    username: str
    email: str
    hashed_password: str

class Post(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    title: str
    content: str
    author_id: uuid.UUID
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class PostCreate(BaseModel):
    title: str
    content: str

class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None