<img width="1833" height="1009" alt="image" src="https://github.com/user-attachments/assets/ccda2673-15ea-4a97-856d-04ff6410c355" />

# MultiTenant Technical Test API

This project is a multi-tenant API for managing **invoices**, **bank transactions**, and reconciliation, implemented in **FastAPI** with **SQLAlchemy**, supporting integration with an LLM (mock AI) for reconciliation explanations.

---

## Requirements

- Docker & Docker Compose
- Python 3.13 (optional if running locally without Docker)
- Alembic for database migrations
- PostgreSQL 16 (container included in Docker Compose)
- `.env` for database configuration

---

## Environment Variables

Create a `.env` file in the project root with:
```env
DB_HOST=db_db
DB_PORT=5432
DB_NAME=*************
DB_USER=************
DB_PASSWORD=**********

API_HOST=0.0.0.0
API_PORT=8000




> Note: Inside the API container, always connect to the **PostgreSQL container host** (`DB_HOST=db`) and the **internal port** (`5432`), not the port exposed on the host.

---

## Starting the Environment with Docker easy apply.

1 - clone the respository:
      git clone <repo_url>
      cd MultiTenant-TechicalTest

2 - Create .env file with your database credentials:
      DB_HOST=db
      DB_PORT=5432
      DB_NAME=tech.........
      DB_USER=tena.........
      DB_PASSWORD=mult.........

3 - execute the command:
      docker compose up --build

      ## Alembic Migrations
4 - Alembic migrations are executed automatically via entrypoint.sh.
      To manually run migrations:
      docker compose run api alembic upgrade head

5 . Access the API:
- Swagger: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## finish the easy apply to start the app.

NOTAS:
  Key Design Decisions and Tradeoffs
    - Multi-Tenant Isolation:
    - All tables (except Tenant) are filtered by tenant_id.
    - Ensures data separation and security at the database level.
  
  AI Integration:
    - AI only explains matches (/explain endpoint) and does not participate in scoring.
    - Uses tenant-authorized data: invoice amount, date, description, transaction info, and heuristic score.
    - Graceful fallback ensures deterministic explanations if AI is unavailable.

  Idempotency:
    - importBankTransactions checks external_id to avoid duplicate inserts.
    - Same idempotency_key with same payload returns the same response; different payload returns conflict error.
  Tradeoffs:
    - AI is mocked initially for simplicity; can be replaced with OpenAI or local LLM.
    - Heuristic scoring is simple (amount match, date tolerance, text similarity) to ensure predictability.
    - Using SQLite locally is sufficient for testing, but PostgreSQL is used for production-like environment.

- Multi-tenant: all operations filtered by `tenant_id`.
- Idempotency: `bank-transactions/import` uses `idempotency_key`.
- Sensitive variables are configured via `.env`.
- API supports automatic migrations and runs from Docker without local dependency installation.


## Main Endpoints
### REST
- `POST /tenants` → Create tenant
- `POST /tenants/{tenant_id}/invoices` → Create invoice
- `DELETE /tenants/{tenant_id}/invoices/{invoice_id}` → Delete invoice
- `POST /tenants/{tenant_id}/bank-transactions/import` → Import transactions (idempotent)
- `POST /tenants/{tenant_id}/reconcile` → Generate reconciliation candidates
- `POST /tenants/{tenant_id}/confirm-match/{match_id}` → Confirm match
- `GET /tenants/{tenant_id}/reconcile/explain?invoice_id=...&transaction_id=...` → AI explanation

### GraphQL (Strawberry)

- Queries:
  - `tenants`
  - `invoices(tenantId, filters, pagination)`
  - `bankTransactions(tenantId, filters, pagination)`
  - `matchCandidates(tenantId, filters)`
  - `explainReconciliation(tenantId, invoiceId, transactionId)`
- Mutations:
  - `createTenant(input)`
  - `createInvoice(tenantId, input)`
  - `deleteInvoice(tenantId, invoiceId)`
  - `importBankTransactions(tenantId, input, idempotencyKey)`
  - `reconcile(tenantId, input?)`
  - `confirmMatch(tenantId, matchId)`

