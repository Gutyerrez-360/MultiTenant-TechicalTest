from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session

from multiTenantApi.core.database import SessionLocal
from multiTenantApi.interfaces.tenantInterface import (
    TenantCreate,
    TenantResponse,
)
from multiTenantApi.services.tenant_service import TenantService
from multiTenantApi.repositories.tenant_repo import TenantRepository

router = APIRouter()

detailMessage = "Tenant mismatch"


def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =========================
# CREATE TENANT (NO TENANT VALIDATION)
# =========================
@router.post(
    "",
    response_model=TenantResponse,
    status_code=201,
)
def create_tenant(
    payload: TenantCreate,
    session: Session = Depends(get_session),
):
    repo = TenantRepository(session)
    service = TenantService(repo)
    return service.create_tenant(payload.name)


# =========================
# LIST TENANTS (NO TENANT VALIDATION)
# =========================
@router.get(
    "",
    response_model=list[TenantResponse],
)
def list_tenants(
    session: Session = Depends(get_session),
):
    repo = TenantRepository(session)
    service = TenantService(repo)
    return service.list_tenants()
