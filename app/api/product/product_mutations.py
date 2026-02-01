import strawberry

@strawberry.type
class ProductMutation:
    @strawberry.field
    def hello(self) -> str:
        return "Hello GraphQL 🚀"
