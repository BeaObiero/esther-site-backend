import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

from app.main import app

client = TestClient(app)

@pytest.fixture
def sample_booking():
    return {
        "full_name": "Esther Waweru",
        "email": "client@example.com",
        "package_type": "Transcription",
        "preferred_date": "2025-08-15",
        "message": "Looking forward to working with you!"
    }

@patch("app.routes.booking.send_email")
def test_booking_success(mock_send_email, sample_booking):
    # Mock email function
    mock_send_email.return_value = True

    response = client.post("/book", json=sample_booking)

    assert response.status_code == 200
    json_data = response.json()
    assert json_data["message"] == "Your booking has been received. We’ll be in touch shortly!"
    assert json_data["data"]["email"] == sample_booking["email"]
    mock_send_email.assert_called_once()
