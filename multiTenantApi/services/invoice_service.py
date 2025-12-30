# services/invoice_service.py
from multiTenantApi.repositories.invoice_repo import InvoiceRepository
from sqlalchemy.orm import Session

class InvoiceService:
    def __init__(self, session: Session):
        self.repo = InvoiceRepository(session)

    def create_invoice(self, tenant_id: int, data: dict):
        return self.repo.create(tenant_id, data)

    def list_invoices(self, tenant_id: int, filters: dict):
        return self.repo.list(tenant_id, filters)

    def delete_invoice(self, tenant_id: int, invoice_id: int):
        return self.repo.delete(tenant_id, invoice_id)
