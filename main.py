import uvicorn
from sqlmodel import create_engine, Session, SQLModel
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from typing import Annotated
from datetime import date
from inventory.repositories import BooksRepository, AuthorRepository
from inventory.inventory_service import InventoryService
from inventory.models import Book, BookResponse, Author, AuthorResponse, Genre, Publisher



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
author_rep = AuthorRepository(engine)
service = InventoryService()


#Book
@app.get("/books", response_model=list[BookResponse])
async def get_books(s: Session = Depends(get_session)):
    books = rep.get_all(s)
    #print (books)
    return books

@app.get("/book/{book_isbn}", response_model=BookResponse)
async def get_book_by_isbn(book_isbn: str, s: Session = Depends(get_session)):
    return rep.get_by_isbn(book_isbn, s) 

@app.delete("/book", response_model=Book)
async def delete_book_by_isbn(book_isbn: str, s: Session = Depends(get_session)): # Darf nichts zurückliefern? 
    
    return rep.delete_by_isbn(book_isbn, s) #{"book:", book_isbn, " deleted"}

@app.post("/book", response_model=Book)
async def create_book(book: Book, s: Session = Depends(get_session)):
    rep.create(book, s)
    return book

@app.put("/book", response_model=Book)
async def update_book(book: Book, s: Session = Depends(get_session)):
    # service.new_author(book, s)
    # service.new_genre(book, s)
    rep.update(book, s)
    return book



#Auhtor
@app.get("/author/{author_id}/books", response_model=list[BookResponse])
async def get_books_by_author(auhtor_id:int, s: Session = Depends(get_session)):
    books = author_rep.get_books_by_id(auhtor_id, s)
    return books

if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
