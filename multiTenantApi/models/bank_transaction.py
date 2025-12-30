from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Numeric,
    Text,
    ForeignKey,
    Index,
    UniqueConstraint,
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from multiTenantApi.models.Base import Base

# =========================
# Bank Transaction, validate transaction 
# =========================
class BankTransaction(Base):
    __tablename__ = "bank_transaction"

    id = Column(Integer, primary_key=True)

    tenant_id = Column(
        Integer,
        ForeignKey("tenant.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    external_id = Column(String(255), nullable=True)
    posted_at = Column(DateTime, nullable=False)

    amount = Column(Numeric(14, 2), nullable=False)
    currency = Column(String(3), default="USD")

    description = Column(Text, nullable=True)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
    )
    deleted_at = Column(DateTime, nullable=True)

    # relationships
    tenant = relationship("Tenant", back_populates="bank_transactions")
    matches = relationship("Match", back_populates="bank_transaction")

    __table_args__ = (
        UniqueConstraint("tenant_id", "external_id", name="uq_bank_tx_external"),
        Index("ix_bank_tx_tenant_posted", "tenant_id", "posted_at"),
    )

    def __repr__(self):
        return f"<BankTransaction id={self.id} amount={self.amount}>"