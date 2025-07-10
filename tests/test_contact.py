import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

from app.main import app

client = TestClient(app)

@pytest.fixture
def sample_contact():
    return {
        "name": "Test User",
        "email": "test@example.com",
        "message": "This is a sample message with enough length."
    }

@patch("app.routes.contact.send_email")
def test_submit_contact(mock_send_email, sample_contact):
    # Mock successful email sending
    mock_send_email.return_value = True

    response = client.post("/contact", json=sample_contact)

    assert response.status_code == 200
    json_data = response.json()
    assert json_data["message"] == "Your message has been received and forwarded."
    assert json_data["data"]["email"] == sample_contact["email"]
    mock_send_email.assert_called_once()
