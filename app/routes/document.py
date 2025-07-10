from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
import shutil
import os
from uuid import uuid4

from app.db.database import get_db
from app.db import models
from app.utils.response_helper import success_response
from app.utils.security import get_current_user

router = APIRouter()

UPLOAD_DIR = "uploads/documents"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload", summary="Upload a document")
def upload_document(
    file: UploadFile = File(...),
    title: str = Form(...),
    description: str = Form(None),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    file_ext = file.filename.split(".")[-1]
    file_name = f"{uuid4()}.{file_ext}"
    file_path = os.path.join(UPLOAD_DIR, file_name)

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        new_doc = models.Document(
            title=title,
            description=description,
            file_path=file_path,
            uploaded_by=current_user.email
        )
        db.add(new_doc)
        db.commit()
        db.refresh(new_doc)

        return success_response(
            message="Document uploaded successfully",
            data={"title": new_doc.title, "id": new_doc.id}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")
