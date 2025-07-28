from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db import models
from app.db.database import get_db
from app.schemas import UserCreate, UserLogin, Token
from app.utils.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    get_current_user,
)
from app.db.models import User as UserModel
from app.utils.response_helper import success_response

router = APIRouter()


@router.post("/register", response_model=Token)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = get_password_hash(user.password)
    new_user = models.User(
        name=user.name,
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_password,
        is_active=True,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    access_token = create_access_token(data={"sub": new_user.email})
    return success_response(
        message="Registration successful",
        data={"access_token": access_token, "token_type": "bearer"}
    )


@router.post("/login", response_model=Token)
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": db_user.email})
    return success_response(
        message="Login successful",
        data={"access_token": access_token, "token_type": "bearer"}
    )


@router.get("/me")
def get_me(current_user: UserModel = Depends(get_current_user)):
    user_data = {
        "id": current_user.id,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "name": current_user.name,
        "is_admin": current_user.is_admin,
        "is_active": current_user.is_active,
    }
    return success_response(
        message="User profile fetched successfully",
        data=user_data
    )


@router.get("/dashboard")
def dashboard(current_user: UserModel = Depends(get_current_user)):
    return success_response(
        message=f"Welcome, {current_user.full_name}!",
        data={"full_name": current_user.full_name}
    )
