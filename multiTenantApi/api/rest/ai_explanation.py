from fastapi import APIRouter, Depends, Query

# orm session
from sqlalchemy.orm import Session

# services
from multiTenantApi.services.ai_explanation_service import ReconciliationService
from multiTenantApi.core.database import SessionLocal

router = APIRouter(prefix="/tenants/{tenant_id}/reconcile")

def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/explain")
def explain_reconciliation(tenant_id: int, invoice_id: int, transaction_id: int, session: Session = Depends(get_session)):
    service = ReconciliationService(session)
    return service.explain_match(tenant_id, invoice_id, transaction_id)