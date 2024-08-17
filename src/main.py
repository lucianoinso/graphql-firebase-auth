import os

from typing import Optional
from typing_extensions import Annotated

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import strawberry
from strawberry.fastapi import GraphQLRouter

from typing import List
from pydantic import BaseModel

import redis
from pymongo import MongoClient
from bson import json_util
from hashlib import sha256

from .auth import IsAuthenticated

FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:4200")
mongo_uri = os.getenv('MONGO_URL', 'mongodb://mongo:27017')
redis_host = os.getenv('REDIS_HOST', 'my_redis')
redis_port = os.getenv('REDIS_PORT', 6379)


# MongoDB setup
mongo_client = MongoClient(mongo_uri)
mongo_db = mongo_client['mydb']

# Redis setup
redis_client = redis.StrictRedis(host=redis_host, port=redis_port, db=0)


@strawberry.type
class User:
    _id: strawberry.ID
    name: str
    gender: str
    age: int
    interests: List[str]
    characteristics: List[str]


def resolve_user(name: str, info: strawberry.Info) -> User:
    cache_key = f"user:{name}"
    cached_user = redis_client.get(cache_key)

    if cached_user:
        user_data = json_util.loads(cached_user)
    else:
        user_data = mongo_db.users.find_one({"name": name})
        if user_data:
            redis_client.set(cache_key, json_util.dumps(user_data), ex=300)

    if user_data:
        return User(**user_data)


async def resolve_users(info: strawberry.Info) -> List[User]:
    cache_key = "users:all"
    cached_users = redis_client.get(cache_key)

    if cached_users:
        users_data = json_util.loads(cached_users)
    else:
        users_data = list(mongo_db.users.find({}))
        if users_data:
            redis_client.set(cache_key,
                             json_util.dumps(users_data, default=str), ex=300)

    return [User(**user_data) for user_data in users_data]


@strawberry.type
class Query:
    user: User = strawberry.field(resolver=resolve_user,
                                  description="Returns a specific user",
                                  permission_classes=[IsAuthenticated])
    users: List[User] = strawberry.field(resolver=resolve_users,
                                         description="Returns list of users",
                                         permission_classes=[IsAuthenticated])


async def get_context():
    return {"test": "test"}

app = FastAPI()

origins = [FRONTEND_URL, "*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

schema = strawberry.Schema(query=Query)

# Authenticate all incoming requests
graphql_app = GraphQLRouter(schema, graphql_ide="graphqli", context_getter=get_context)

# graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")


@app.get("/")
def home():
    return {"Hello": "world"}
