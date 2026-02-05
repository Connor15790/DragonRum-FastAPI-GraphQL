import strawberry

from .auth.auth_mutations import AuthMutation
from .auth.auth_query import AuthQuery

from .product.product_mutations import ProductMutation
from .product.product_query import ProductQuery

from .cart.cart_mutations import CartMutation
from .cart.cart_query import CartQuery

@strawberry.type
class Query(AuthQuery, ProductQuery, CartQuery): 
    pass

@strawberry.type
class Mutation(AuthMutation, ProductMutation, CartMutation):
    pass

schema = strawberry.Schema(query=Query, mutation=Mutation)