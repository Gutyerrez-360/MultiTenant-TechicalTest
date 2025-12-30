from fastapi import FastAPI

# schema of graphQL
from strawberry.fastapi import GraphQLRouter
from multiTenantApi.api.graphQL.schema import schema

# multitenant of rest
from multiTenantApi.api.rest import (
    tenants,
    invoices,
    bank_transactions,
    reconciliation,
    ai_explanation
)

# Middleware
from multiTenantApi.middleware.tenant import TenantMiddleware

app = FastAPI(title="Multi Tenant API")

# Applying the middleware
app.add_middleware(TenantMiddleware)


graphql_app = GraphQLRouter(schema, graphiql=True)
app.include_router(graphql_app, prefix="/graphql")

# REST routers, the prefix /tenants is required in the whole routers
app.include_router(tenants.router, prefix="/tenants", tags=["Tenants"])
app.include_router(invoices.router, tags=["Invoices"])
app.include_router(bank_transactions.router, tags=["Bank Transactions"])
app.include_router(reconciliation.router, tags=["Reconciliation"])
app.include_router(ai_explanation.router, tags=['AI-Explanation'])

# this functions is just for testing app
@app.get("/health")
def health():
    return {"status": "ok"}
