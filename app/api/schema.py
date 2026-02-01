import strawberry

from .auth.auth_mutations import AuthMutation
from .auth.auth_query import AuthQuery

from .product.product_mutations import ProductMutation
from .product.product_query import ProductQuery

@strawberry.type
class Query(AuthQuery, ProductQuery): 
    pass

class Mutation(AuthMutation, ProductMutation):
    pass

schema = strawberry.Schema(query=Query, mutation=Mutation)