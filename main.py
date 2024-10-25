from sqlmodel import create_engine, Session, SQLModel
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from typing import Annotated
from datetime import date
from .inventory.repositories.books_repository import BooksRepository
from .inventory.inventory_service import InventoryService
from .inventory.models.book import Book 
from .inventory.models.author import Author
from .inventory.models.genre import Genre
from .inventory.models.publisher import Publisher


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



rep = BooksRepository(engine)
service = InventoryService()


@app.get("/books", response_model=list[Book])
async def get_books():
    return rep.get_all()

@app.get("/book/{book_isbn}", response_model=Book)
async def get_book_by_isbn(book_isbn: int):
    rep.get_by_isbn(book_isbn)
    return {"book_isbn": book_isbn}

@app.delete("/book", response_model=Book)
async def delete_book_by_isbn(book_isbn: int):
    rep.delete_by_isbn(book_isbn)
    return {"book:", book_isbn, " deleted"}

@app.post("/book", response_model=Book)
async def create_book(book: Book):
    rep.create(book)
    return book

@app.put("/book", response_model=Book)
async def update_book(book: Book):
    service.new_author(book)
    service.new_genre(book)
    rep.update(book)
    return book