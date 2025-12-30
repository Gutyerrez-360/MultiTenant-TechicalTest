from sqlalchemy import select
from sqlalchemy.orm import Session

# http response
from fastapi import HTTPException

from multiTenantApi.models.tenant import Tenant


class TenantRepository:
    def __init__(self, session: Session):
        self.session = session

    # =========================
    # CREATE FUNCTION LOGIC with conection on database REQUIRED FUNCTION
    # =========================
    def create(self, name: str) -> Tenant:
        if not name or name.strip() == "":
            # lanzar error con status 400
            raise HTTPException(status_code=400, detail="Name is required")
        try:
            tenant = Tenant(name=name)
            self.session.add(tenant)
            self.session.commit()
            self.session.refresh(tenant)
            return tenant
        except Exception as error:
            return error

    # =========================
    # LIST OPTIONAL FUNCTION
    # =========================
    def list(self) -> list[Tenant]:
        try:
            stmt = select(Tenant).where(Tenant.deleted_at.is_(None))
            result = self.session.execute(stmt)
            return result.scalars().all()
        except Exception as error:
            return error
