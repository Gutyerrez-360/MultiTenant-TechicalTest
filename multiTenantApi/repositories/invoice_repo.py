# repositories/invoice_repo.py
from sqlalchemy import select, and_
from sqlalchemy.orm import Session
from sqlalchemy import func

from multiTenantApi.models.invoice import Invoice
from multiTenantApi.models.vendor import Vendor


class InvoiceRepository:
    def __init__(self, session: Session):
        self.session = session

    # =========================
    # CREATE FUNCTION LOGIC REQUIRED FUNCTION
    # =========================
    def create(self, tenant_id: int, data: dict):
        try:
            vendor_id = data.get("vendor_id")

            # validate vendor_id
            if vendor_id is not None:
                stmt = select(Vendor).where(Vendor.id == vendor_id)
                vendor = self.session.execute(stmt).scalar_one_or_none()
                if not vendor:
                    # return value if it a not found result
                    return {"error": True, "message": f"This vendor id: {vendor_id} not found"}

            allowed_status = [Invoice.STATUS_OPEN, Invoice.STATUS_MATCHED, Invoice.STATUS_PAID]
            status = data.get("status", Invoice.STATUS_OPEN)
            if status not in allowed_status:
                return {"error": True, "message": f"Invalid status '{status}'. Allowed values: {allowed_status}"}

            # creat bill
            invoice = Invoice(
                tenant_id=tenant_id,
                vendor_id=vendor_id,
                invoice_number=data.get("invoice_number"),
                amount=data["amount"],
                currency=data.get("currency", "USD"),
                invoice_date=data.get("invoice_date"),
                description=data.get("description"),
                status=data.get("status", "open"),
            )

            self.session.add(invoice)
            self.session.commit()
            self.session.refresh(invoice)

            return invoice

        except Exception as e:
            self.session.rollback()
            return {"error": True, "message": str(e)}


    # =========================
    # LIST FUNCTION LOGIC (with required filters) REQUIRED FUNCTION
    # =========================
    def list(self, tenant_id: int, filters: dict) -> list[Invoice]:
        try:
            stmt = select(Invoice).where(
                and_(
                    Invoice.tenant_id == tenant_id,
                    Invoice.deleted_at.is_(None),
                )
            )

            # ---- filters ----
            if filters.get("status"):
                stmt = stmt.where(Invoice.status == filters["status"])

            if filters.get("vendor_id"):
                stmt = stmt.where(Invoice.vendor_id == filters["vendor_id"])

            if filters.get("amount_min"):
                stmt = stmt.where(Invoice.amount >= filters["amount_min"])

            if filters.get("amount_max"):
                stmt = stmt.where(Invoice.amount <= filters["amount_max"])

            if filters.get("date_from"):
                stmt = stmt.where(Invoice.invoice_date >= filters["date_from"])

            if filters.get("date_to"):
                stmt = stmt.where(Invoice.invoice_date <= filters["date_to"])

            result = self.session.execute(stmt)
            return result.scalars().all()
        except Exception as error:
            return error

    # =========================
    # DELETE FUNCTION LOGIC (soft delete) REQUIRED FUNCTION
    # =========================
    def delete(self, tenant_id: int, invoice_id: int) -> None:
        try:
            stmt = select(Invoice).where(
                and_(
                    Invoice.id == invoice_id,
                    Invoice.tenant_id == tenant_id,
                    Invoice.deleted_at.is_(None),
                )
            )

            invoice = self.session.execute(stmt).scalar_one_or_none()

            if not invoice:
                raise ValueError("Invoice not found")

            invoice.deleted_at = func.now()
            invoice.updated_at = func.now()


            self.session.commit()
        except Exception as error:
                    return error