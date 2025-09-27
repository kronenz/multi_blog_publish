from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from datetime import datetime

class BlogPost(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    vault_id: UUID
    title: str
    content: str
    status: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
