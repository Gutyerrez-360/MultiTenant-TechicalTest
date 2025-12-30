from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from multiTenantApi.models.Base import Base

#Entity in the database
class Tenant(Base):
    __tablename__ = "tenant"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
    )
    deleted_at = Column(DateTime, nullable=True)

    vendors = relationship("Vendor", back_populates="tenant")
    matches = relationship("Match", back_populates="tenant")
    bank_transactions = relationship("BankTransaction", back_populates="tenant")
    invoices = relationship("Invoice", back_populates="tenant")
