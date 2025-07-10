import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.database import Base, get_db
from app.db.models import User
from app.utils.security import get_current_user

# ----------- Test DB Setup -----------
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_admin.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(bind=engine)

Base.metadata.create_all(bind=engine)

# ----------- Mock Admin User -----------
def override_get_current_user():
    return User(
        id=1,
        email="admin@example.com",
        full_name="Admin Test",
        is_admin=True,
        hashed_password="testpass"
    )

app.dependency_overrides[get_db] = lambda: TestingSessionLocal()
app.dependency_overrides[get_current_user] = override_get_current_user

client = TestClient(app)

# ----------- Tests -----------
def test_get_all_users():
    response = client.get("/admin/users")
    assert response.status_code == 200
    assert "data" in response.json()

def test_get_all_documents():
    response = client.get("/admin/documents")
    assert response.status_code == 200
    assert "data" in response.json()

def test_filter_invoices():
    response = client.get("/admin/invoices/filter")
    assert response.status_code == 200
    assert isinstance(response.json().get("data"), list)

def test_invoice_report():
    response = client.get("/admin/report/invoices")
    assert response.status_code == 200
    assert "data" in response.json()
