# middleware/tenant.py
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from fastapi.responses import JSONResponse

PUBLIC_PATHS = (
    "/health",
    "/docs",
    "/openapi.json",
    "/redoc",
    "/graphql",

)

SPECIAL_PATH = (
    "/tenants"
)

class TenantMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path = request.url.path

        if path.startswith(PUBLIC_PATHS):
            return await call_next(request)
        
        if SPECIAL_PATH in path:
            return await call_next(request)

        
        # get tenant id in the params
        tenant_id = (request.headers.get("X-Tenant-ID"))

        if not tenant_id:
            return JSONResponse(
                status_code=400,
                content={"detail": "Tenant ID is required"},
            )

        #parse value for tenant_id
        request.state.tenant_id = int(tenant_id)
        return await call_next(request)
