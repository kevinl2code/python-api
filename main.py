import json
import os
from typing import Literal, Optional
from uuid import uuid4
from fastapi import FastAPI, HTTPException
import random
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from mangum import Mangum
from app.db.postgres_client import get_postgres_client
from contextlib import asynccontextmanager
from app.routers import user, conversation


@asynccontextmanager
async def lifespan(app: FastAPI):
    postgres_client = get_postgres_client()
    postgres_client.connect()
    yield
    postgres_client.disconnect()


# class Book(BaseModel):
#     name: str
#     genre: Literal["fiction", "non-fiction"]
#     price: float
#     book_id: Optional[str] = uuid4().hex


# BOOKS_FILE = "books.json"
# BOOKS = []

# if os.path.exists(BOOKS_FILE):
#     with open(BOOKS_FILE, "r") as f:
#         BOOKS = json.load(f)

app = FastAPI()
app.include_router(user.router)
app.include_router(conversation.router)
handler = Mangum(app)


# @app.get("/")
# async def root():
#     return {"message": "Welcome to my bookstore app!"}


# @app.get("/random-book")
# async def random_book():
#     return random.choice(BOOKS)


# @app.get("/list-books")
# async def list_books():
#     return {"books": BOOKS}


# @app.get("/book_by_index/{index}")
# async def book_by_index(index: int):
#     if index < len(BOOKS):
#         return BOOKS[index]
#     else:
#         raise HTTPException(
#             404, f"Book index {index} out of range ({len(BOOKS)}).")


# @app.post("/add-book")
# async def add_book(book: Book):
#     book.book_id = uuid4().hex
#     json_book = jsonable_encoder(book)
#     BOOKS.append(json_book)

#     with open(BOOKS_FILE, "w") as f:
#         json.dump(BOOKS, f)

#     return {"book_id": book.book_id}


# @app.get("/get-book")
# async def get_book(book_id: str):
#     for book in BOOKS:
#         if book.book_id == book_id:
#             return book

#     raise HTTPException(404, f"Book ID {book_id} not found in database.")
