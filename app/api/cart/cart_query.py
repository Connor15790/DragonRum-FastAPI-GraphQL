import strawberry
import jwt
import os
from typing import Optional
from app.database import db
from .cart_types import CartItemType, CartType
from bson import ObjectId

JWT_SECRET = os.getenv("JWT_SECRET")
cart_collection = db.get_collection("carts")

@strawberry.type
class CartQuery:
    @strawberry.field
    async def get_cart(self, info) -> Optional[CartType]:
        request = info.context["request"]
        token = request.cookies.get("token")
        if not token:
            raise Exception("Unauthorized!")
        
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
            user_id_str = payload.get("id")
            user_id = ObjectId(user_id_str)

            print("JWT PAYLOAD:", payload)
            print("ID TYPE:", type(payload.get("id")))

            cart = await cart_collection.find_one({"userId": user_id})
            if not cart:
                return CartType(userId=user_id, items=[], totalPrice=0)
            
            items = [
                CartItemType(
                    productId=str(item["productId"]),
                    name=item["name"],
                    price=float(item["price"]),
                    image=item["image"],
                    quantity=item["quantity"]
                )
                for item in cart.get("items", [])
            ]
            totalPrice = cart.get("totalPrice")

            return CartType(userId=user_id, items=items, totalPrice=totalPrice)
        except Exception as e:
            print("ERROR:", e)
            raise