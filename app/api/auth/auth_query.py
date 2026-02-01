import strawberry
import jwt
import os
from typing import Optional
from app.database import user_collection
from bson import ObjectId

JWT_SECRET = os.getenv("JWT_SECRET")

@strawberry.type
class UserType:
    id: str
    name: str
    email: str
    createdAt: str
    updatedAt: str

@strawberry.type
class AuthQuery:
    @strawberry.field
    async def me(self, info) -> Optional[UserType]:
        request = info.context["request"]
        token = request.cookies.get("token")

        if not token:
            return None 

        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
            user_id = payload.get("id")

            user = await user_collection.find_one({"_id": ObjectId(user_id)})

            if not user:
                return None

            return UserType(
                id=str(user["_id"]),
                name=user["name"],
                email=user["email"],
                createdAt=user["createdAt"].isoformat(),
                updatedAt=user["updatedAt"].isoformat()
            )

        except Exception:
            return None