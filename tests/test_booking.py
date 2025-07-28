import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app

client = TestClient(app)

@pytest.fixture
def sample_booking():
    return {
        "email": "client@example.com",
        "full_name": "Esther Waweru",
        "message": "Looking forward to working with you!",
        "package_type": "Transcription",
        "preferred_date": "2025-08-10T00:00:00"  # ISO format string
    }

@patch("app.routes.booking.send_email")
def test_booking_success(mock_send_email, sample_booking):
    mock_send_email.return_value = True

    # Send booking request
    response = client.post("/api/book", json=sample_booking)

    # Check status and structure
    assert response.status_code == 200
    json_data = response.json()

    assert json_data["message"] == "Your booking has been received. We’ll be in touch shortly!"
    assert json_data["data"]["email"] == sample_booking["email"]
    assert json_data["data"]["preferred_date"] == sample_booking["preferred_date"]
    assert json_data["data"]["full_name"] == sample_booking["full_name"]
    assert json_data["data"]["package_type"] == sample_booking["package_type"]
    assert json_data["data"]["message"] == sample_booking["message"]

    # Check email was sent
    mock_send_email.assert_called_once()
