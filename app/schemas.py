from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


# ---- User Schemas ----
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    full_name: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    full_name: Optional[str]
    is_admin: Optional[bool] = False

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


# ---- Booking Schemas ----
class BookingCreate(BaseModel):
    full_name: str = Field(..., min_length=2)
    email: EmailStr
    package_type: str  # e.g., "Essential", "Premium", etc.
    preferred_date: datetime
    message: Optional[str] = Field(None, max_length=500)


class BookingOut(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    package_type: str
    preferred_date: datetime
    message: Optional[str]

    class Config:
        from_attributes = True


# ---- Contact Schema ----
class ContactForm(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    email: EmailStr
    message: str = Field(..., min_length=10, max_length=1000)


# ---- Optional: Document and Invoice Output Schemas ----
class DocumentOut(BaseModel):
    id: int
    filename: str
    filepath: str
    uploaded_at: datetime
    user_id: int

    class Config:
        from_attributes = True


class InvoiceOut(BaseModel):
    id: int
    description: str
    file_path: str
    created_at: datetime
    paid: bool
    user_id: int

    class Config:
        from_attributes = True
