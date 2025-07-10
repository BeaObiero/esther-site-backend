from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import shutil
import os
from datetime import datetime

from app.db.database import get_db
from app.utils.security import get_current_user
from app.db.models import User, Document, Invoice
from app.utils.response_helper import success_response

router = APIRouter()


# ---- 1. View All Documents (Admin) ----
@router.get("/admin/documents")
def get_all_documents(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    documents = db.query(Document).filter(Document.user_id == current_user.id).all()
    return success_response("Documents retrieved successfully", documents)


# ---- 2. Upload a Document ----
@router.post("/admin/upload-document")
def upload_document(file: UploadFile = File(...), current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    file_location = f"uploads/{file.filename}"
    os.makedirs("uploads", exist_ok=True)

    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    new_doc = Document(
        filename=file.filename,
        filepath=file_location,
        user_id=current_user.id
    )
    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)

    return success_response("Document uploaded successfully", {
        "filename": file.filename,
        "path": file_location
    })


# ---- 3. Delete a Document ----
@router.delete("/admin/documents/{doc_id}")
def delete_document(doc_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    doc = db.query(Document).filter_by(id=doc_id, user_id=current_user.id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    if os.path.exists(doc.filepath):
        os.remove(doc.filepath)

    db.delete(doc)
    db.commit()
    return success_response("Document deleted successfully", {"deleted_id": doc_id})


# ---- 4. Filter Invoices by Status or Date ----
@router.get("/admin/invoices/filter")
def filter_invoices(
    status: Optional[str] = Query(None),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(Invoice).filter(Invoice.user_id == current_user.id)

    if status:
        query = query.filter(Invoice.status == status)

    if start_date:
        query = query.filter(Invoice.created_at >= datetime.fromisoformat(start_date))
    if end_date:
        query = query.filter(Invoice.created_at <= datetime.fromisoformat(end_date))

    filtered_invoices = query.all()
    return success_response("Filtered invoices retrieved successfully", filtered_invoices)


# ---- 5. Generate Downloadable Report ----
@router.get("/admin/report/invoices")
def invoice_report(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    invoices = db.query(Invoice).filter(Invoice.user_id == current_user.id).all()
    report = [
        {
            "invoice_id": invoice.id,
            "amount": invoice.amount,
            "status": invoice.status,
            "uploaded_at": invoice.uploaded_at.strftime("%Y-%m-%d")
        }
        for invoice in invoices
    ]
    return success_response("Invoice report generated", report)
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import shutil
import os
from datetime import datetime

from app.db.database import get_db
from app.utils.security import get_current_user
from app.db.models import User, Document, Invoice
from app.utils.response_helper import success_response

router = APIRouter()


# ---- 1. View All Documents (Admin) ----
@router.get("/admin/documents")
def get_all_documents(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized")

    documents = db.query(Document).all()
    result = [{
        "id": doc.id,
        "filename": doc.filename,
        "filepath": doc.filepath,
        "uploaded_at": doc.uploaded_at.isoformat(),
        "user_id": doc.user_id
    } for doc in documents]

    return success_response("Documents retrieved successfully", result)


# ---- 2. Upload a Document ----
@router.post("/admin/upload-document")
def upload_document(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized")

    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    new_doc = Document(
        filename=file.filename,
        filepath=file_path,
        uploaded_at=datetime.utcnow(),
        user_id=current_user.id
    )
    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)

    return success_response("Document uploaded successfully", {
        "filename": file.filename,
        "path": file_path
    })


# ---- 3. Delete a Document ----
@router.delete("/admin/documents/{doc_id}")
def delete_document(
    doc_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized")

    doc = db.query(Document).filter(Document.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    if os.path.exists(doc.filepath):
        os.remove(doc.filepath)

    db.delete(doc)
    db.commit()

    return success_response("Document deleted successfully", {"deleted_id": doc_id})


# ---- 4. Filter Invoices by Paid Status or Date ----
@router.get("/admin/invoices/filter")
def filter_invoices(
    paid: Optional[bool] = Query(None),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized")

    query = db.query(Invoice)

    if paid is not None:
        query = query.filter(Invoice.paid == paid)
    if start_date:
        query = query.filter(Invoice.created_at >= datetime.fromisoformat(start_date))
    if end_date:
        query = query.filter(Invoice.created_at <= datetime.fromisoformat(end_date))

    results = [{
        "id": inv.id,
        "description": inv.description,
        "file_path": inv.file_path,
        "created_at": inv.created_at.isoformat(),
        "paid": inv.paid,
        "user_id": inv.user_id
    } for inv in query.all()]

    return success_response("Filtered invoices retrieved successfully", results)


# ---- 5. Generate Downloadable Invoice Report ----
@router.get("/admin/report/invoices")
def invoice_report(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized")

    invoices = db.query(Invoice).all()
    report = [{
        "invoice_id": inv.id,
        "description": inv.description,
        "created_at": inv.created_at.strftime("%Y-%m-%d"),
        "paid": inv.paid
    } for inv in invoices]

    return success_response("Invoice report generated", report)


# ----6. Get All Users ----
@router.get("/admin/users")
def get_all_users(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized")

    users = db.query(User).all()
    user_list = [{
        "id": user.id,
        "email": user.email,
        "full_name": user.full_name,
        "is_admin": user.is_admin
    } for user in users]

    return success_response("User list retrieved", user_list)