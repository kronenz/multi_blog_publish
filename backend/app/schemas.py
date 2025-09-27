from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
import uuid

class PostBase(BaseModel):
    title: str
    content: str

class PostCreate(PostBase):
    pass

class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

class Post(PostBase):
    id: uuid.UUID
    author_id: uuid.UUID
    created_at: datetime

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: uuid.UUID
    posts: List[Post] = []

    class Config:
        orm_mode = True

# To handle the circular dependency between User and Post
User.update_forward_refs()
Post.update_forward_refs()

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None