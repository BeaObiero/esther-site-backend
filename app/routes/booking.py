from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.utils.email_sender import send_email
from app.utils.response_helper import success_response
from app.schemas import BookingCreate, BookingOut

router = APIRouter()

@router.post("/book", response_model=BookingOut)
def book_session(payload: BookingCreate, db: Session = Depends(get_db)):
    try:
        # 1. Email notification
        subject = f"New Booking - {payload.package_type}"
        body = (
            f"Booking Details:\n"
            f"Name: {payload.full_name}\n"
            f"Email: {payload.email}\n"
            f"Package: {payload.package_type}\n"
            f"Preferred Date: {payload.preferred_date}\n"
            f"Message: {payload.message or 'N/A'}"
        )
        send_email("shi3.waweru@gmail.com", subject, body)

        # 2. Convert datetime to string for safe JSON response
        booking_data = payload.model_dump()
        booking_data["preferred_date"] = payload.preferred_date.isoformat()

        return success_response(
            message="Your booking has been received. We’ll be in touch shortly!",
            data=booking_data
        )

    except Exception as e:
        print(f"Booking error: {e}") 
        raise HTTPException(status_code=500, detail=f"Booking failed: {str(e)}")
