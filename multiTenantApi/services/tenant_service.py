from multiTenantApi.repositories.tenant_repo import TenantRepository


class TenantService:
    def __init__(self, repo: TenantRepository):
        self.repo = repo

    def create_tenant(self, name: str):
        return self.repo.create(name)

    def list_tenants(self):
        return self.repo.list()
