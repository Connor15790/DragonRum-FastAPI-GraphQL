import strawberry

@strawberry.type
class CartMutation:
    @strawberry.field
    def hello(self) -> str:
        return "Hello GraphQL 🚀"
