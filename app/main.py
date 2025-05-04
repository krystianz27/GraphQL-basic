import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from graphene import Schema
from starlette_graphene3 import (
    GraphQLApp,
    make_graphiql_handler,
    make_playground_handler,
)

from app.db.database import prepare_database
from app.db.db_middleware import DBSessionMiddleware
from app.gql.context import get_context
from app.gql.mutations import Mutation
from app.gql.queries import Query
from app.routes import employers, jobs

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
schema = Schema(query=Query, mutation=Mutation)


@asynccontextmanager
async def lifespan(app: FastAPI):
    prepare_database()
    yield


app = FastAPI(lifespan=lifespan)
app.add_middleware(DBSessionMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(employers.router)
app.include_router(jobs.router)


@app.get("/")
def root():
    return {
        "message": "Welcome to the API!",
        "endpoints": {
            "test": "/test",
            "graphql": "/graphql",
            "graphqlPlayground": "/playground",
        },
    }


@app.get("/test")
def test_endpoint():
    return {"message": "Test successful"}


app.mount(
    "/graphql",
    GraphQLApp(
        schema=schema,
        on_get=make_graphiql_handler(),
        context_value=get_context,
    ),
)

app.mount(
    "/playground",
    GraphQLApp(
        schema=schema,
        on_get=make_playground_handler(),
        context_value=get_context,
    ),
)
