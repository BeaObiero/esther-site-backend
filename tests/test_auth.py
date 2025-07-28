import pytest
from fastapi.testclient import TestClient
from app.main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.models import Base
import uuid

# --- Setup Test Database ---
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_auth.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(bind=engine)

Base.metadata.create_all(bind=engine)

client = TestClient(app)

# --- Fixtures ---
@pytest.fixture
def test_user():
    return {
        "name": "Test Name",
        "email": "testuser@example.com",
        "password": "testpassword123",
        "full_name": "Test User"
    }

# --- Tests ---
def test_register_user():
    unique_email = f"user_{uuid.uuid4().hex}@example.com"
    test_user = {
        "name": "Test Name",
        "email": unique_email,
        "full_name": "Test User",
        "password": "testpassword123"
    }
    response = client.post("/api/auth/register", json=test_user)
    assert response.status_code == 200
    assert "access_token" in response.json()["data"]

def test_login_user(test_user):
    client.post("/api/auth/register", json=test_user)
    response = client.post("/api/auth/login", json={
        "email": test_user["email"],
        "password": test_user["password"]
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data["data"]
    assert data["message"] == "Login successful"

def test_get_me(test_user):
    client.post("/api/auth/register", json=test_user)
    login_resp = client.post("/api/auth/login", json={
        "email": test_user["email"],
        "password": test_user["password"]
    })
    assert login_resp.status_code == 200
    token = login_resp.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/api/auth/me", headers=headers)
    assert response.status_code == 200
    assert response.json()["data"]["email"] == test_user["email"]

def test_dashboard(test_user):
    client.post("/api/auth/register", json=test_user)
    login_resp = client.post("/api/auth/login", json={
        "email": test_user["email"],
        "password": test_user["password"]
    })
    token = login_resp.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/api/auth/dashboard", headers=headers)
    assert response.status_code == 200
    assert "Welcome" in response.json()["message"]
