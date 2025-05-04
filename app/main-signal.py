import asyncio
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

from app.background_tasks.user_events import process_user_created_queue
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
    asyncio.create_task(process_user_created_queue())
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


@app.get("/test")
async def test_endpoint():
    return {"message": "Test successful"}


# Automatically close db, no need to db.close() Middleware
app.mount(
    "/graphql",
    GraphQLApp(
        schema=schema,
        on_get=make_graphiql_handler(),
        context_value=get_context,
    ),
)

app.mount(
    "/graphqlplayground",
    GraphQLApp(
        schema=schema,
        on_get=make_playground_handler(),
        context_value=lambda request: {"request": request},
    ),
)
