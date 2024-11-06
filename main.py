import uvicorn
from sqlmodel import create_engine, Session, SQLModel
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from typing import Annotated
from datetime import date
from inventory.repositories import BooksRepository, AuthorRepository, GenreRepository, PublisherRepository
from inventory.inventory_service import InventoryService
from inventory.models import Book, BookResponse, BookCreate, Author, AuthorResponse, Genre, Publisher



sql_url = "postgresql://postgres:admin@localhost:5431/db"

connect_args = {"check_same_thread": False}
engine = create_engine(sql_url, echo=True)
session = Session(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield



app = FastAPI(lifespan=lifespan)



rep = BooksRepository(session)
author_rep = AuthorRepository(session)
genre_rep = GenreRepository(session)
publisher_rep = PublisherRepository(session)
service = InventoryService(session)


#Book
@app.get("/books", response_model=list[BookResponse])
async def get_books():
    books = rep.get_all()
    #print (books)
    return books

@app.get("/book/{book_isbn}", response_model=BookResponse)
async def get_book_by_isbn(book_isbn: str):
    return rep.get_by_isbn(book_isbn) 

@app.delete("/book/{isbn}", response_model=Book)
async def delete_book_by_isbn(isbn: str): 
    return rep.delete_by_isbn(isbn) 

@app.post("/book", response_model=BookResponse)
async def create_book(book: BookCreate):
    return rep.create(book)

@app.put("/book/{isbn}", response_model=Book)
async def update_book(isbn: str, new_book :Book):
    # service.new_author(book, s)
    # service.new_genre(book, s)
    
    return rep.update(isbn, new_book)



#Auhtor
@app.get("/author/{author_id}/books", response_model=list[Book])
async def get_books_by_author(auhtor_id:int):
    return author_rep.get_books_by_id(auhtor_id)



#Genre
@app.get("/genre/{genre_id}/books", response_model= list[Book])
async def get_books_by_genre(genre_id: int):
    return genre_rep.get_books_by_id(genre_id)



#Publisher
@app.get("/publisher/{publisher_id}/books", response_model= list[Book])
async def get_books_by_genre(publisher_id: int):
    return publisher_rep.get_books_by_id(publisher_id)



if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
