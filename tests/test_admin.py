import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.database import Base, get_db
from app.db.models import User
from app.utils.security import get_password_hash, create_access_token

# ----------- Setup Test Database -----------
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_admin.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(bind=engine)

Base.metadata.create_all(bind=engine)

# ----------- Dependency Override -----------
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# ----------- Test Client -----------
client = TestClient(app)

# ----------- Helper Function to Get Admin Token -----------
def get_admin_token():
    db = TestingSessionLocal()
    user = db.query(User).filter(User.email == "admin@example.com").first()
    if not user:
        user = User(
            name="Admin",
            full_name="Admin User",
            email="admin@example.com",
            hashed_password=get_password_hash("adminpass"),
            is_admin=True
        )
        db.add(user)
        db.commit()
    db.close()
    return create_access_token(data={"sub": "admin@example.com"})

# ----------- Auth Header -----------
def auth_headers():
    token = get_admin_token()
    return {"Authorization": f"Bearer {token}"}

# ----------- Tests -----------
def test_get_all_users():
    response = client.get("/api/admin/users", headers=auth_headers())
    assert response.status_code == 200
    assert "data" in response.json()

def test_get_all_documents():
    response = client.get("/api/admin/documents", headers=auth_headers())
    assert response.status_code == 200
    assert "data" in response.json()

def test_filter_invoices():
    response = client.get("/api/admin/invoices/filter", headers=auth_headers())
    assert response.status_code == 200
    assert isinstance(response.json()["data"], (dict, list))

def test_invoice_report():
    response = client.get("/api/admin/report/invoices", headers=auth_headers())
    assert response.status_code == 200
    assert "data" in response.json()
