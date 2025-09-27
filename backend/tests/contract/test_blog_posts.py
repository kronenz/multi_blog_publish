from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

from uuid import uuid4

def test_create_blog_post():
    vault_id = str(uuid4())
    response = client.post("/blog_posts", json={"vault_id": vault_id, "title": "test_post", "content": "test_content", "status": "draft"})
    assert response.status_code == 201
