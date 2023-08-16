import json

from typing import Any, List, TypedDict
from pypika import PostgreSQLQuery, Table
from fastapi import APIRouter
from pydantic import BaseModel

from app.db.pg_tables import UsersTable
from app.db.postgres_client import get_postgres_client
from app.lc import question_agent
from datetime import datetime

from app.lc.sdk.pinecone import test_pinecone


router = APIRouter()


class TypedMessge(TypedDict):
    created_at: int
    user_message: str
    ai_message: str


class Message:
    def __init__(self, created_at: int, user_message: str, ai_message: str):
        self.created_at = created_at
        self.user_message = user_message
        self.ai_message = ai_message

    def to_dict(self) -> TypedMessge:
        return {
            'created_at': self.created_at,
            'user_message': self.user_message,
            'ai_message': self.ai_message
        }


def fetch_data(query: str) -> Any:
    try:
        client = get_postgres_client()
        client.connect()
        result = client.fetch_data(query)
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


@router.post("/converse")
async def converse(user_message: str, user_id: str, location: str) -> Any:
    # get user from db
    user_query = PostgreSQLQuery.from_(UsersTable).select(
        "*").where(UsersTable.id == user_id)
    user = fetch_data(user_query.get_sql())
    conversation: List[Message] = user[0]['conversation']

    # get user's conversation and preferences
    # if no location use user's selected city
    # hit question agent
    # return response
    # update conversation in db

    try:
        print('conversation: ', conversation)
        response = question_agent(user_message, conversation)
        print('response: ', response)
        current_timestamp = int(datetime.now().timestamp())
        message = Message(
            created_at=current_timestamp, user_message=user_message, ai_message=response).to_dict()
        # print('conversation: ', type(conversation))
        conversation.append(message)

        discourse_query = PostgreSQLQuery.update(UsersTable).set(
            UsersTable.conversation, json.dumps(conversation)).where(UsersTable.id == user_id)
        execute_query(discourse_query.get_sql())
        # print('response: ', response)

    except Exception as e:
        print(f'e: {e}')
    # conversation = json.dumps(conversation)
    # location = json.dumps(location)

    # query = PostgreSQLQuery.into(UsersTable).columns("firstname", "lastname", "email", "type", "conversation", "location").insert(
    #     user.first_name, user.last_name, user.email, 'USER', conversation, location)
    # execute_query(query.get_sql())


# @router.get("/user/{user_id}")
# async def get_user(user_id: int) -> Any:

#     query = PostgreSQLQuery.from_(UsersTable).select(
#         "*").where(UsersTable.id == user_id)
#     print('query: ', query.get_sql())
#     fetch_data(query.get_sql())


@router.post("/converseee")
async def test():
    test_pinecone()
