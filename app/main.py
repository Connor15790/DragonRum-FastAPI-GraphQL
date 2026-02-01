from fastapi import FastAPI, Response, Request
from strawberry.fastapi import GraphQLRouter
from app.api.schema import schema

async def get_context(request: Request, response: Response):
    return {"request": request, "response": response}

graphql_app = GraphQLRouter(schema, context_getter=get_context)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")