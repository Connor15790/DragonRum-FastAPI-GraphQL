import strawberry
from typing import List, Optional

@strawberry.type
class CartItemType:
    productId: str
    name: str
    price: float
    image: Optional[str] = None
    quantity: int

@strawberry.type
class CartType:
    userId: str
    items: List[CartItemType]
    totalPrice: float