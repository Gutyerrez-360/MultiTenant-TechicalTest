
from fastapi import APIRouter, Depends, Request, HTTPException, Header
from sqlalchemy.orm import Session
from typing import List

from multiTenantApi.core.database import SessionLocal
from multiTenantApi.services.bank_transaction_service import BankTransactionService
from multiTenantApi.interfaces.bankTransactionInterface import BankTransactionCreate

# prefix required for indications in the challenge
router = APIRouter(
    prefix="/tenants/{tenant_id}/bank-transactions"
)

def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/import")
def import_bank_transactions(
    tenant_id: int,
    payload: List[BankTransactionCreate],
    idempotency_key: str = Header(...),
    session: Session = Depends(get_session),
):
    service = BankTransactionService(session)
    return service.bulk_import(tenant_id, payload, idempotency_key)
