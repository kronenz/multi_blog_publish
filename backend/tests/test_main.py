import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker
from app.main import app, get_db
from app.database import Base
import os

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
    # Create a user first
    client.post(
        "/users/",
        json={"email": "test@example.com", "username": "testuser", "password": "password"},
    )
    # Try to create the same user again
    response = client.post(
        "/users/",
        json={"email": "test@example.com", "username": "testuser", "password": "password"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Email already registered"}

def test_login_for_access_token():
    # Create a user to log in with
    client.post(
        "/users/",
        json={"email": "test@example.com", "username": "testuser", "password": "password"},
    )
    # Log in
    response = client.post(
        "/token",
        data={"username": "testuser", "password": "password"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_read_users_me():
    # Create user and get token
    client.post(
        "/users/",
        json={"email": "test@example.com", "username": "testuser", "password": "password"},
    )
    login_response = client.post(
        "/token",
        data={"username": "testuser", "password": "password"},
    )
    token = login_response.json()["access_token"]

    # Access protected route
    response = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}