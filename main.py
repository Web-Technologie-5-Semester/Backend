from fastapi.responses import JSONResponse
import uvicorn
from sqlmodel import create_engine, Session, SQLModel
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, Request
from typing import Annotated
from datetime import date
from inventory.repositories import BooksRepository, AuthorRepository, GenreRepository, PublisherRepository
from inventory.inventory_service import BookService, AuthorService, GenreService, PublisherService
from inventory.models import AuthorCreate, Book, BookResponse, BookCreate, Author, AuthorResponse, Genre, GenreCreate, GenreResponse, Publisher, PublisherCreate, PublisherResponse
from user.models import Role, User
from inventory.exception import  ForbiddenException, NotFoundException



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

@app.exception_handler(NotFoundException)
async def not_found_handler(request: Request, exc: NotFoundException):
    return JSONResponse(
        status_code=404,
        content= {"message": exc.to_string()}
    )

@app.exception_handler(ForbiddenException)
async def forbidden_handler(request: Request, exc: ForbiddenException):
    return JSONResponse(
        status_code= 403,
        content= {"message": exc.to_string()}
    )

book_service = BookService(session)
author_service = AuthorService(session)
genre_service = GenreService(session)
publisher_service = PublisherService(session)


#Book
@app.get("/books", response_model=list[BookResponse])
async def get_books():
    books = book_service.get_all_books()
    return books

@app.get("/book/{isbn}", response_model=BookResponse)
async def get_book_by_isbn(isbn: str):
    book= book_service.get_book_by_isbn(isbn)
    # if book is None or isbn != book.isbn:
    #     raise BookException(isbn=isbn)
    return book

@app.delete("/book/{isbn}", response_model=Book)
async def delete_book_by_isbn(isbn: str): 
    return book_service.delete_book_by_isbn(isbn) 

@app.post("/book", response_model=BookResponse)
async def create_book(book: BookCreate):
    return book_service.create(book)

@app.put("/book/{isbn}", response_model=Book)
async def update_book(isbn: str, new_book :Book):
    return book_service.update(isbn, new_book)

#such endpunkt
@app.post("/search", response_model=list[Book])
async def search(word: str):
    return book_service.search_book(word)


#Auhtor
@app.get("/author", response_model=list[Author])
async def get_authors():
    return author_service.get_all_authors()

@app.get("/author/{author_id}/books", response_model=list[Book])
async def get_books_by_author(auhtor_id:int):
    return author_service.get_books_by_author(auhtor_id)

@app.delete("/author/{author_id}", response_model=Author)
async def delete_author_by_id(id: int): 
    return author_service.delete_author_by_id(id) 

@app.post("/author", response_model=AuthorResponse)
async def create_author(author: AuthorCreate):
    return author_service.create(author)

@app.put("/author/{author_id}", response_model=Author)
async def update_author(id: int, new_author: Author):
    return author_service.update(id, new_author)


#Genre
@app.get("/genre", response_model=list[Genre])
async def get_genres():
    return genre_service.get_all_genres()

@app.get("/genre/{genre_id}/books", response_model= list[Book])
async def get_books_by_genre(genre_id: int):
    return genre_service.get_books_by_genre(genre_id)

@app.delete("/genre/{genre_id}", response_model=Genre)
async def delete_genre_by_id(id: int): 
    return genre_service.delete_genre_by_id(id) 

@app.post("/genre", response_model=GenreResponse)
async def create_genre(genre: GenreCreate):
    return genre_service.create(genre)

@app.put("/genre/{genre_id}", response_model=Genre)
async def update_genre(id: int, new_genre: Genre):
    return genre_service.update(id, new_genre)


#Publisher
@app.get("/publisher", response_model=list[Publisher])
async def get_publishers():
    return publisher_service.get_all_publishers()

@app.get("/publisher/{publisher_id}/books", response_model= list[Book])
async def get_books_by_genre(publisher_id: int):
    return publisher_service.get_books_by_publisher(publisher_id)

@app.delete("/publisher/{publisher_id}", response_model=Publisher)
async def delete_publisher_by_id(id: int): 
    return publisher_service.delete_author_by_id(id) 

@app.post("/publisher", response_model=PublisherResponse)
async def create_author(publisher: PublisherCreate):
    return publisher_service.create(publisher)

@app.put("/publisher/{publisher_id}", response_model=Publisher)
async def update_author(id: int, new_publisher: Publisher):
    return publisher_service.update(id, new_publisher)


#############################################################################
# @app.get("/users", response_model=list[User])
# async def get_all_users():
#     return user_rep.get_all()

if __name__=="__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
