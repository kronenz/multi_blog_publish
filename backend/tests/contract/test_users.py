from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_create_user():
    response = client.post("/users", json={"name": "test", "email": "test@example.com", "password": "password"})
    assert response.status_code == 201
