import strawberry
from fastapi import Response
from datetime import datetime, timezone

from app.database import db
from app.auth.utils import hash_password, verify_password, create_access_token

user_collection = db.get_collection("users")


@strawberry.type
class AuthResponse:
    message: str
    success: bool


@strawberry.type
class AuthMutation:
    @strawberry.mutation
    async def login(self, info, email: str, password: str) -> AuthResponse:
        user = await user_collection.find_one({"email": email.lower().strip()})

        if user is None:
            raise Exception("Invalid email or password")

        if not verify_password(password, user["password"]):
            raise Exception("Invalid email or password")

        token = create_access_token({"id": str(user["_id"])})

        

        response: Response = info.context["response"]
        response.set_cookie(key="token", value=token, httponly=True)

        return AuthResponse(message="Logged in successfully", success=True)

    @strawberry.mutation
    async def signup(self, info, name: str, email: str, password: str) -> AuthResponse:
        existing_user = await user_collection.find_one({"email": email})
        if existing_user:
            raise Exception("Email already exists!")

        hashed_password = hash_password(password)

        now = datetime.now(timezone.utc)
        result = await user_collection.insert_one(
            {
                "name": name,
                "email": email.lower().strip(),
                "password": hashed_password,
                "createdAt": now,
                "updatedAt": now,
            }
        )

        token = create_access_token({"id": str(result.inserted_id)})

        response: Response = info.context["response"]
        response.set_cookie(key="token", value=token, httponly=True, samesite="lax")

        return AuthResponse(message="Successfully signed up", success=True)

    @strawberry.mutation
    async def logout(self, info) -> AuthResponse:
        response: Response = info.context["response"]

        response.delete_cookie(key="token", path="/", httponly=True, samesite="lax")

        return AuthResponse(message="Logged out successfuly", success=True)
