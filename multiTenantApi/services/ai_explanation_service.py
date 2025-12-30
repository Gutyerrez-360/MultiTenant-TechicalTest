from multiTenantApi.repositories.reconciliation_repo import ReconciliationRepository
from fastapi import HTTPException
import os

# Simular AI client (puedes cambiar por OpenAI o cualquier LLM)
def mock_ai_explanation(context: dict) -> dict:
    """
    Devuelve explicación mock de reconciliación.
    """
    try:
        explanation = (
            f"Invoice {context['invoice_number']} of amount {context['invoice_amount']} "
            f"matches transaction {context['transaction_id']} posted at {context['transaction_date']}. "
            f"Score heurístico: {context['score']}."
        )
        return {"explanation": explanation, "confidence": 0.9}
    except Exception:
        return None

class ReconciliationService:
    def __init__(self, session):
        self.repo = ReconciliationRepository(session)

    def explain_match(self, tenant_id: int, invoice_id: int, transaction_id: int):
        invoice, txn = self.repo.get_invoice_and_transaction(tenant_id, invoice_id, transaction_id)

        # calcular heurístico simple
        score = 0
        if invoice.amount == txn.amount:
            score += 100
        elif abs(invoice.amount - txn.amount) <= 1.0:
            score += 80

        if invoice.invoice_date and txn.posted_at:
            date_diff = abs((invoice.invoice_date - txn.posted_at.date()).days)
            if date_diff <= 3:
                score += 10

        # Context for AI mock
        context = {
            "invoice_id": invoice.id,
            "invoice_number": invoice.invoice_number,
            "invoice_amount": float(invoice.amount),
            "invoice_date": str(invoice.invoice_date),
            "transaction_id": txn.id,
            "transaction_amount": float(txn.amount),
            "transaction_date": str(txn.posted_at),
            "score": score,
            "invoice_description": invoice.description,
            "transaction_description": txn.description,
        }

        # calling th AI (mock) for processing the results
        try:
            ai_response = mock_ai_explanation(context)
            if ai_response:
                return ai_response
        except Exception:
            pass

        # # fall with specific an concrets results
        fallback = f"Invoice {invoice.id} likely matches transaction {txn.id} with score {score}."
        return {"explanation": fallback, "confidence": None}