from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from multiTenantApi.services.reconciliation_service import ReconciliationService
from multiTenantApi.core.database import SessionLocal

router = APIRouter(prefix="/tenants/{tenant_id}")

def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/reconcile")
def reconcile(tenant_id: int, session: Session = Depends(get_session)):
    service = ReconciliationService(session)
    return service.run_reconciliation(tenant_id)

@router.post("/matches/{match_id}/confirm")
def confirm_match(tenant_id: int, match_id: int, session: Session = Depends(get_session)):
    service = ReconciliationService(session)
    return service.confirm_match(tenant_id, match_id)