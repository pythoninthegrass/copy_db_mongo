#!/usr/bin/env python

from fastapi import FastAPI, APIRouter
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

app = FastAPI(title="FastAPI - MongoDB")

ALLOWED_HOSTS = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# cf. https://github.com/markqiu/fastapi-mongodb-realworld-example-app/tree/master/app
# TODO: fill out
def connect_to_mongo():
    pass


# TODO: fill out
def close_mongo_connection():
    pass


# TODO: fill out
def http_error_handler():
    pass


# TODO: fill out
def http_422_error_handler():
    pass


app.add_event_handler("startup", connect_to_mongo)
app.add_event_handler("shutdown", close_mongo_connection)


app.add_exception_handler(HTTPException, http_error_handler)
app.add_exception_handler(HTTP_422_UNPROCESSABLE_ENTITY, http_422_error_handler)

api_router = APIRouter()

app.include_router(api_router, prefix="/api")
