from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_user_registration_and_login():
    # Register a new user
    response = client.post("/users", json={"name": "test_user", "email": "test_user@example.com", "password": "password"})
    assert response.status_code == 201

    # Login with the new user
    response = client.post("/token", data={"username": "test_user@example.com", "password": "password"})
    assert response.status_code == 200
    assert "access_token" in response.json()
