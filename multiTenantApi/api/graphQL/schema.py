import strawberry
from multiTenantApi.api.graphQL.query import Query

schema = strawberry.Schema(query=Query)
