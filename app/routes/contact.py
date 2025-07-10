from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.utils.email_sender import send_email
from app.utils.response_helper import success_response

router = APIRouter()




@router.post("/contact", status_code=200)
def submit_contact(form: ContactForm, db: Session = Depends(get_db)):
    subject = f"New Contact from {form.name}"
    body = f"Message:\n{form.message}\n\nReply to: {form.email}"

    try:
        send_email("shi3.waweru@gmail.com", subject, body)
        return success_response(
            message="Your message has been received and forwarded.",
            data=form.model_dump()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send message: {str(e)}")
