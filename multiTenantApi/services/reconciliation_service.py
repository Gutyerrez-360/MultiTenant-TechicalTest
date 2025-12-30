from sqlalchemy.orm import Session
from multiTenantApi.repositories.reconciliation_repo import ReconciliationRepository

class ReconciliationService:
    def __init__(self, session: Session):
        self.repo = ReconciliationRepository(session)

    def run_reconciliation(self, tenant_id: int):
        return self.repo.generate_candidates(tenant_id)

    def confirm_match(self, tenant_id: int, match_id: int):
        return self.repo.confirm_match(tenant_id, match_id)