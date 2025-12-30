from multiTenantApi.models.invoice import Invoice
from multiTenantApi.models.bank_transaction import BankTransaction
from multiTenantApi.models.match import Match

# manage responde in except
from fastapi import HTTPException

class ReconciliationRepository:
    def __init__(self, session):
        self.session = session

    def generate_candidates(self, tenant_id: int):
        # ejemplo heurística simple: match exact amount y fecha ±3 días
        invoices = self.session.query(Invoice).filter_by(tenant_id=tenant_id, deleted_at=None).all()
        transactions = self.session.query(BankTransaction).filter_by(tenant_id=tenant_id).all()

        candidates = []
        for inv in invoices:
            for txn in transactions:
                if not inv.invoice_date or not txn.created_at:
                    continue
                score = 0
                if inv.amount == txn.amount:
                    score += 100
                elif abs(inv.amount - txn.amount) <= 1.0:  # range for tolerance
                    score += 80

                if abs((inv.invoice_date - txn.created_at.date()).days) <= 3:
                    score += 10 # plus in al score puntage

                # creation simple before the validations
                if score > 0:
                    candidates.append({
                        "invoice_id": inv.id,
                        "transaction_id": txn.id,
                        "score": score,
                        "status": "proposed"
                    })
        return candidates

    # confirm match
    def confirm_match(self, tenant_id: int, match_id: int):
        match = self.session.query(Match).filter_by(id=match_id, tenant_id=tenant_id).first()
        if not match:
            raise HTTPException(status_code=404, detail="Match not found")
        match.status = "confirmed"
        self.session.commit()
        return {"status": "ok", "message": f"Match {match_id} confirmed"}
    
    
    # Apply filter by specific situations
    def get_invoice_and_transaction(self, tenant_id: int, invoice_id: int, transaction_id: int):
        invoice = (
            self.session.query(Invoice)
            .filter(
                Invoice.id == invoice_id,
                Invoice.tenant_id == tenant_id,
                Invoice.deleted_at.is_(None)
            )
            .first()
        )
        txn = (
            self.session.query(BankTransaction)
            .filter(
                BankTransaction.id == transaction_id,
                BankTransaction.tenant_id == tenant_id,
                BankTransaction.deleted_at.is_(None)
            )
            .first()
        )

        if not invoice or not txn:
            raise HTTPException(
                status_code=404,
                detail="Invoice or Transaction not found for this tenant"
            )

        return invoice, txn
