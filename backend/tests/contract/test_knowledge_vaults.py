from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

from uuid import uuid4

def test_create_knowledge_vault():
    user_id = str(uuid4())
    response = client.post("/knowledge_vaults", json={"user_id": user_id, "name": "test_vault"})
    assert response.status_code == 201
