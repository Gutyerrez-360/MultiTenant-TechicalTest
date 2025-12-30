from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Index,
    UniqueConstraint,
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from multiTenantApi.models.Base import Base

# =========================
# Class Vendor require table
# =========================
class Vendor(Base):
    __tablename__ = "vendor"

    id = Column(Integer, primary_key=True)

    tenant_id = Column(
        Integer,
        ForeignKey("tenant.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    name = Column(String(255), nullable=False)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
    )
    deleted_at = Column(DateTime, nullable=True)

    tenant = relationship("Tenant", back_populates="vendors")
    invoices = relationship("Invoice", back_populates="vendor")

    __table_args__ = (
        UniqueConstraint("tenant_id", "name", name="uq_vendor_name"),
        Index("ix_vendor_tenant_name", "tenant_id", "name"),
    )

    def __repr__(self):
        return f"<Vendor {self.name}>"