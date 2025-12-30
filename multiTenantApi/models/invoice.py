# fucntions django
from sqlalchemy import func
# schemas sqlalchemy
from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    DateTime,
    ForeignKey,
    Numeric,
    Index,
)
from multiTenantApi.models.Base import Base
from sqlalchemy.orm import relationship


# =========================
# Class Invoice required table
# =========================    
from sqlalchemy import CheckConstraint

class Invoice(Base):
    __tablename__ = "invoice"

    STATUS_OPEN = "open"
    STATUS_MATCHED = "matched"
    STATUS_PAID = "paid"

    STATUS_CHOICES = [STATUS_OPEN, STATUS_MATCHED, STATUS_PAID]

    id = Column(Integer, primary_key=True)
    tenant_id = Column(Integer, ForeignKey("tenant.id"), nullable=False)
    vendor_id = Column(Integer, ForeignKey("vendor.id"), nullable=True)

    invoice_number = Column(String(100))
    amount = Column(Numeric(14, 2), nullable=False)
    currency = Column(String(3), default="USD")
    invoice_date = Column(Date, nullable=True)
    description = Column(String, nullable=True)
    status = Column(
        String(20),
        default=STATUS_OPEN,
        nullable=False,
    )

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now())
    deleted_at = Column(DateTime, nullable=True)

    tenant = relationship("Tenant", back_populates="invoices")
    vendor = relationship("Vendor", back_populates="invoices")
    matches = relationship("Match", back_populates="invoice") 

    __table_args__ = (
        Index("ix_invoice_tenant_status", "tenant_id", "status"),
        Index("ix_invoice_tenant_number", "tenant_id", "invoice_number"),
        CheckConstraint(
            status.in_(STATUS_CHOICES), 
            name="ck_invoice_status_valid"
        ),
    )
