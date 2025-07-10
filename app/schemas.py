from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class BookingCreate(BaseModel):
    full_name: str = Field(..., min_length=2)
    email: EmailStr
    package_type: str  # e.g., "Essential", "Premium", etc.
    preferred_date: datetime
    message: str = Field(None, max_length=500)

class BookingOut(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    package_type: str
    preferred_date: datetime
    message: str | None

class Config:
    from_attributes = True  # Updated for Pydantic v2


class ContactForm(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    email: EmailStr
    message: str = Field(..., min_length=10, max_length=1000)