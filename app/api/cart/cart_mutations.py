import strawberry
import jwt
import os
from app.database import db
from .cart_types import CartItemType, CartType
from strawberry.types import Info
from bson import ObjectId

JWT_SECRET = os.getenv("JWT_SECRET")
cart_collection = db.get_collection("carts")


@strawberry.type
class CartMutation:
    async def get_user_id(info):
        token = info.context["request"].cookies.get("token")
        if not token:
            raise Exception("Unauthorized!")
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        return payload.get("id")

    @strawberry.mutation
    async def add_item_to_cart(
        self, info, productId: str, name: str, price: float, image: str, quantity: int
    ) -> CartType:
        user_id = await CartMutation.get_user_id(info)
        item_total = price * quantity
        new_item = {
            "productId": productId,
            "name": name,
            "price": price,
            "image": image,
            "quantity": quantity,
        }

        user_cart = await cart_collection.find_one({"userId": ObjectId(user_id)})

        if not user_cart:
            await cart_collection.insert_one(
                {
                    "userId": ObjectId(user_id),
                    "items": [new_item],
                    "totalPrice": item_total,
                }
            )
        else:
            items = user_cart.get("items", [])
            item_index = next(
                (i for i, item in enumerate(items) if item["productId"] == productId),
                -1,
            )

            if item_index > -1:
                items[item_index]["quantity"] += quantity
            else:
                items.append(new_item)

            new_total_price = sum(
                float(item["price"]) * item["quantity"] for item in items
            )

            await cart_collection.update_one(
                {"userId": ObjectId(user_id)},
                {"$set": {"items": items, "totalPrice": new_total_price}},
            )

        updated_cart = await cart_collection.find_one({"userId": ObjectId(user_id)})

        return CartType(
            userId=str(updated_cart["userId"]),
            items=[
                CartItemType(
                    productId=str(item["productId"]),
                    name=item["name"],
                    price=float(item["price"]),
                    image=item.get("image"),
                    quantity=item["quantity"],
                )
                for item in updated_cart["items"]
            ],
            totalPrice=updated_cart["totalPrice"],
        )

    @strawberry.mutation
    async def update_item_in_cart(
        self, info, productId: str, quantity: int
    ) -> CartType:
        user_id = await CartMutation.get_user_id(info)

        user_cart = await cart_collection.find_one({"userId": ObjectId(user_id)})

        if not user_cart:
            raise Exception("Cart does not exist!")

        items = user_cart.get("items", [])
        item_index = next(
            (i for i, item in enumerate(items) if item["productId"] == productId), -1
        )

        if item_index == -1:
            raise Exception("Item does not exist!")

        if quantity == 1:
            items[item_index]["quantity"] += 1
        else:
            if items[item_index]["quantity"] == 1:
                items.pop(item_index)
            else:
                items[item_index]["quantity"] -= 1

        new_total_price = sum(float(item["price"]) * item["quantity"] for item in items)

        await cart_collection.update_one(
            {"userId": ObjectId(user_id)},
            {"$set": {"items": items, "totalPrice": new_total_price}},
        )

        updated_cart = await cart_collection.find_one({"userId": ObjectId(user_id)})

        return CartType(
            userId=str(updated_cart["userId"]),
            items=[
                CartItemType(
                    productId=str(item["productId"]),
                    name=item["name"],
                    price=float(item["price"]),
                    image=item.get("image"),
                    quantity=item["quantity"],
                )
                for item in updated_cart["items"]
            ],
            totalPrice=updated_cart["totalPrice"],
        )

    @strawberry.mutation
    async def clear_cart(self, info) -> str:
        user_id = await CartMutation.get_user_id(info)

        user_cart = await cart_collection.find_one({"userId": ObjectId(user_id)})

        if not user_cart:
            raise Exception("Cart does not exist!")

        await cart_collection.find_one_and_delete({"userId": ObjectId(user_id)})

        return "Cart Cleared"
