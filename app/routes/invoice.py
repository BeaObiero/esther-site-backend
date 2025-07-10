from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from datetime import datetime
import os
import uuid

from app.db.database import get_db
from app.db import models
from app.utils.email_sender import send_email
from app.utils.response_helper import success_response
from app.utils.security import get_current_user

router = APIRouter()

INVOICE_DIR = "uploads/invoices"
os.makedirs(INVOICE_DIR, exist_ok=True)

@router.post("/generate", summary="Generate and optionally send invoice")
def generate_invoice(
    client_email: str,
    service_description: str,
    amount_kes: float,
    send_via_email: bool = True,
    background_tasks: BackgroundTasks = Depends(),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    try:
        invoice_id = str(uuid.uuid4())
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"invoice_{invoice_id}_{timestamp}.txt"
        file_path = os.path.join(INVOICE_DIR, filename)

        content = f"""
        INVOICE
        -------
        ID: {invoice_id}
        Issued By: {current_user.full_name} ({current_user.email})
        Client Email: {client_email}
        Service: {service_description}
        Amount: KES {amount_kes}
        Date: {timestamp}
        """

        # Save file
        with open(file_path, "w") as file:
            file.write(content.strip())

        # Store metadata in DB
        invoice = models.Invoice(
            client_email=client_email,
            service_description=service_description,
            amount_kes=amount_kes,
            file_path=file_path,
            created_by=current_user.email,
        )
        db.add(invoice)
        db.commit()
        db.refresh(invoice)

        if send_via_email:
            subject = "Your Invoice"
            body = f"Dear client,\n\nPlease find attached your invoice for: {service_description}.\n\nThank you!"
            background_tasks.add_task(send_email, client_email, subject, body, file_path)

        return success_response(
            message="Invoice generated successfully.",
            data={"invoice_id": invoice.id, "file_path": file_path}
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Invoice generation failed: {str(e)}")
