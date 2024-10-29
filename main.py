import uvicorn
from sqlmodel import create_engine, Session, SQLModel
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from typing import Annotated
from datetime import date
from inventory.repositories import BooksRepository
from inventory.inventory_service import InventoryService
from inventory.models import Book, BookResponse, Author, Genre, Publisher



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


@app.get("/books", response_model=list[BookResponse])
async def get_books():
    books = rep.get_all()
    #print (books)
    return books

@app.get("/book/{book_isbn}", response_model=Book)
async def get_book_by_isbn(book_isbn: int):
    return rep.get_by_isbn(book_isbn)

# @app.get("/book/{author}", response_model=Book)
# async def get_book_by_author(book_author: str):
#     return rep.get_by_author(book_author)

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

if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
