from sqlmodel import create_engine, Session, SQLModel, Field
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from typing import Annotated
from datetime import date
from .inventory.repositories.books_repository import BooksRepository
from .inventory import books_router
from .inventory.models.books import Book 


sql_url = "postgresql://postgres:admin@localhost:5431/db"

connect_args = {"check_same_thread": False}
engine = create_engine(sql_url, echo=True)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield



app = FastAPI(lifespan=lifespan)

# app.include_router(books_router)


rep = BooksRepository(engine)


@app.get("/books")
async def get_books():
    return rep.get_all()

@app.get("/books/{book_isbn}")
async def get_book_by_isbn(book_isbn: int):
    rep.get_by_isbn(book_isbn)
    return {"book_isbn": book_isbn}

@app.delete("/books")
async def delete_book_by_isbn(book_isbn: int):
    rep.delete_by_isbn(book_isbn)
    return {"book:", book_isbn, " deleted"}

@app.post("/books")
async def create_book(book: Book):
    rep.create(book)
    return book

@app.put("/books")
async def update_book(book: Book):
    rep.update(book)
    return book