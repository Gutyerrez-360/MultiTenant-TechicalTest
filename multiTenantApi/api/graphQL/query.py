import strawberry

@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        return "Hello from MultiTenant GraphQL, this is a test"
