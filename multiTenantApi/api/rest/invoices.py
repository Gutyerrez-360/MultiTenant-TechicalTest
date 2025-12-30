# api/invoices.py
from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session

from multiTenantApi.core.database import SessionLocal
from multiTenantApi.services.invoice_service import InvoiceService

# interfaces
from multiTenantApi.interfaces.invoiceInterface import InvoiceCreate

router = APIRouter(
    prefix="/tenants/{tenant_id}/invoices"
)
detailMessage = "Tenant mismatch"

# Dependency
def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("")
def list_invoices(
    tenant_id: int,
    status: str | None = None,
    session: Session = Depends(get_session),
):
 
    service = InvoiceService(session)
    return service.list_invoices(
        tenant_id,
        {"status": status},
    )

@router.post("")
def create_invoice(
    tenant_id: int,
    payload: InvoiceCreate,
    session: Session = Depends(get_session),
):
    service = InvoiceService(session)
    return service.create_invoice(tenant_id, payload.dict())


@router.delete("/{invoice_id}")
def delete_invoice(
    tenant_id: int,
    invoice_id: int,
    session: Session = Depends(get_session),
):
    service = InvoiceService(session)
    service.delete_invoice(tenant_id, invoice_id)
    return {"status": "deleted"}
