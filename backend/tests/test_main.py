import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker
from app.main import app, get_db
from app.database import Base
import os
import uuid

# In-memory Test Database
SQLALCHEMY_DATABASE_URL = "sqlite://"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the get_db dependency to use the test database
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Fixture to create a new database for each test function
@pytest.fixture(autouse=True)
def setup_and_teardown_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

client = TestClient(app)

# Helper function to create a user and get a token
def create_user_and_get_token(username, password, email):
    client.post(
        "/users/",
        json={"email": email, "username": username, "password": password},
    )
    login_response = client.post(
        "/token",
        data={"username": username, "password": password},
    )
    return login_response.json()["access_token"]

def test_create_user():
    response = client.post(
        "/users/",
        json={"email": "test@example.com", "username": "testuser", "password": "password"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data
    assert "posts" in data

def test_create_duplicate_user():
    client.post("/users/", json={"email": "test@example.com", "username": "testuser", "password": "password"})
    response = client.post("/users/", json={"email": "test@example.com", "username": "testuser", "password": "password"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Email already registered"}

def test_login_for_access_token():
    create_user_and_get_token("testuser", "password", "test@example.com")
    response = client.post("/token", data={"username": "testuser", "password": "password"})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_read_users_me():
    token = create_user_and_get_token("testuser", "password", "test@example.com")
    response = client.get("/users/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"

def test_create_post():
    token = create_user_and_get_token("testuser", "password", "test@example.com")
    response = client.post(
        "/posts/",
        headers={"Authorization": f"Bearer {token}"},
        json={"title": "Test Post", "content": "This is a test post."},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Post"
    assert "id" in data
    assert "author_id" in data

def test_read_posts():
    token = create_user_and_get_token("testuser", "password", "test@example.com")
    client.post("/posts/", headers={"Authorization": f"Bearer {token}"}, json={"title": "Test Post", "content": "Content"})
    response = client.get("/posts/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Test Post"

def test_update_own_post():
    token = create_user_and_get_token("testuser", "password", "test@example.com")
    create_response = client.post("/posts/", headers={"Authorization": f"Bearer {token}"}, json={"title": "Old Title", "content": "Old"})
    post_id = create_response.json()["id"]

    response = client.put(
        f"/posts/{post_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"title": "New Title"},
    )
    assert response.status_code == 200
    assert response.json()["title"] == "New Title"

def test_delete_own_post():
    token = create_user_and_get_token("testuser", "password", "test@example.com")
    create_response = client.post("/posts/", headers={"Authorization": f"Bearer {token}"}, json={"title": "To Delete", "content": "Content"})
    post_id = create_response.json()["id"]

    delete_response = client.delete(f"/posts/{post_id}", headers={"Authorization": f"Bearer {token}"})
    assert delete_response.status_code == 200

    get_response = client.get(f"/posts/{post_id}")
    assert get_response.status_code == 404

def test_update_other_user_post():
    user1_token = create_user_and_get_token("user1", "pw1", "user1@test.com")
    user2_token = create_user_and_get_token("user2", "pw2", "user2@test.com")

    create_response = client.post("/posts/", headers={"Authorization": f"Bearer {user1_token}"}, json={"title": "User1 Post", "content": ""})
    post_id = create_response.json()["id"]

    response = client.put(f"/posts/{post_id}", headers={"Authorization": f"Bearer {user2_token}"}, json={"title": "Updated by User2"})
    assert response.status_code == 403

def test_publish_post():
    token = create_user_and_get_token("testuser", "password", "test@example.com")
    create_response = client.post("/posts/", headers={"Authorization": f"Bearer {token}"}, json={"title": "Publish Test", "content": ""})
    post_id = create_response.json()["id"]

    response = client.post(f"/posts/{post_id}/publish", headers={"Authorization": f"Bearer {token}"}, json={"platform": "tistory"})
    assert response.status_code == 200
    assert "Post published to tistory" in response.json()["message"]

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}