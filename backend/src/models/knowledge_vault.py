from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from datetime import datetime

class KnowledgeVault(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    user_id: UUID
    name: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
