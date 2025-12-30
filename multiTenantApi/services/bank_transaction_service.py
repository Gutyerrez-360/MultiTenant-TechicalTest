from sqlalchemy.orm import Session
from typing import List
from multiTenantApi.models.bank_transaction import BankTransaction
from multiTenantApi.repositories.bank_transaction_repo import BankTransactionRepository
from multiTenantApi.interfaces.bankTransactionInterface import BankTransactionCreate

class BankTransactionService:
    def __init__(self, session: Session):
        self.repo = BankTransactionRepository(session)

    def bulk_import(self, tenant_id: int, transactions: List[BankTransactionCreate], idempotency_key: str):
        # using logic bulk for creation list in cascade mode
        return self.repo.bulk_create(tenant_id, transactions, idempotency_key)
