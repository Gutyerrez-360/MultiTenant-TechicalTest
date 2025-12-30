from sqlalchemy import select
from sqlalchemy.orm import Session
from multiTenantApi.models.bank_transaction import BankTransaction
from multiTenantApi.models.tenant import Tenant

# manage responde in except
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError


class BankTransactionRepository:
    def __init__(self, session: Session):
        self.session = session

    def bulk_create(self, tenant_id: int, transactions, idempotency_key: str):
        try:
            # validate idempotency_key
            stmt_tenant = select(Tenant).where(Tenant.id == tenant_id)
            tenant = self.session.execute(stmt_tenant).scalar_one_or_none()
            if not tenant:
                raise HTTPException(
                    status_code=404,
                    detail={"status": False, "message": f"Tenant with id {tenant_id} does not exist"}
                )

            created = []
            for txn in transactions:

                obj = BankTransaction(
                    tenant_id=tenant_id,
                    external_id=txn.external_id,
                    amount=txn.amount,
                    currency=txn.currency,
                    posted_at=txn.transaction_date,
                    description=txn.description,
                )
                self.session.add(obj)
                created.append(obj)

            self.session.commit()
            return {
                "status": True,
                "message": f"{len(created)} transactions imported",
                "transactions": [t.id for t in created]
            }

        except IntegrityError as e:
            self.session.rollback()
            # Detectamos si es por unique constraint
            if "uq_bank_tx_external" in str(e.orig):
                raise HTTPException(
                    status_code=400,
                    detail={"status": False, "message": "Duplicate transaction external_id for this tenant"}
                )
            raise HTTPException(
                status_code=400,
                detail={"status": False, "message": str(e)}
            )
        except Exception as error:
            self.session.rollback()
            raise HTTPException(status_code=400, detail={"status": False, "message": str(error)})