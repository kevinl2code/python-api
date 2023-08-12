import json

from typing import Any
from pypika import PostgreSQLQuery, Table
from fastapi import APIRouter
from pydantic import BaseModel
from app.db.pg_tables import UsersTable
from app.db.postgres_client import get_postgres_client


router = APIRouter()


class User(BaseModel):
    first_name: str
    last_name: str
    email: str
    interests: list[int]


def fetch_data(query: str) -> Any:
    try:
        client = get_postgres_client()
        client.connect()
        result = client.fetch_data(query)
        print(f'result: {result}')
        client.disconnect()

        return result
    except Exception as e:
        print(f'e: {e}')


def execute_query(query: str) -> Any:
    try:
        client = get_postgres_client()
        client.connect()
        result = client.execute_query(query)
        client.disconnect()

        return result
    except Exception as e:
        print(f'e: {e}')


@router.post("/user")
async def create_user(user: User) -> Any:

    location = {
        'city': 'Austin',
        'state': 'TX'
    }

    conversation = []
    conversation = json.dumps(conversation)
    location = json.dumps(location)

    query = PostgreSQLQuery.into(UsersTable).columns("firstname", "lastname", "email", "type", "conversation", "location").insert(
        user.first_name, user.last_name, user.email, 'USER', conversation, location)
    execute_query(query.get_sql())


@router.get("/user/{user_id}")
async def get_user(user_id: int) -> Any:

    query = PostgreSQLQuery.from_(UsersTable).select(
        "*").where(UsersTable.id == user_id)
    print('query: ', query.get_sql())
    fetch_data(query.get_sql())
