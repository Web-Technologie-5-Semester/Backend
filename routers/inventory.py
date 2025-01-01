from fastapi import APIRouter, Depends, Response
from sqlmodel import Session
from constants import SELLER_ROLE
from inventory.models import Author, AuthorCreate, AuthorResponse, Book, BookCreate, BookResponse, Genre, GenreCreate, GenreResponse, Publisher, PublisherCreate, PublisherResponse
from inventory.inventory_service import BookService, AuthorService, GenreService, PublisherService
from db import get_session
from user.role_checker import role_checker_factory
from user.service import UserService
from user.models import User
from typing import Annotated

inv_router = APIRouter()


#Book
@inv_router.get("/books", response_model=list[BookResponse])
async def get_books(session: Session = Depends(get_session)):
    books = BookService(session).get_all_books()
    return books

@inv_router.get("/book/{isbn}", response_model=BookResponse)
async def get_book_by_isbn(isbn: str, session: Session = Depends(get_session)):
    book= BookService(session).get_book_by_isbn(isbn)
    return book

@inv_router.delete("/book/{isbn}")
async def delete_book_by_isbn(
    isbn: str,
    _: bool = Depends(role_checker_factory(allowed_roles=[SELLER_ROLE])),
    session: Session = Depends(get_session)
):
    return BookService(session).delete_book_by_isbn(isbn)


@inv_router.post("/book", response_model=BookResponse)
async def create_book(
    book: BookCreate,
    _: Annotated[bool, Depends(role_checker_factory(allowed_roles=[SELLER_ROLE]))], 
    session: Session = Depends(get_session)):
    return BookService(session).create(book)
                                 
@inv_router.put("/book/{isbn}", response_model=Book)
async def update_book(
    isbn: str, 
    new_book :Book, 
    _: bool = Depends(role_checker_factory(allowed_roles=[SELLER_ROLE])),
    session: Session = Depends(get_session)):
    return BookService(session).update(isbn, new_book)
                                 
#such endpunkt
@inv_router.get("/search", response_model=list[BookResponse])
async def search(word: str, session: Session = Depends(get_session)):
    return BookService(session).search_book(word)

@inv_router.get("/book/{isbn}/recommendations", response_model=list[BookResponse])
async def get_recommendations(isbn: str, session: Session = Depends(get_session)):
    return BookService(session).get_recommendations_for(isbn)

@inv_router.get("/book/{isbn}/image", 
    responses = {
        200: {
            "content": {"image/jpeg": {}}
        }
    },
    response_class=Response
)
async def get_image(isbn: str, session: Session = Depends(get_session)):
    bytes = BookService(session).get_image(isbn)
    return Response(content=bytes, media_type="image/jpeg")

#Auhtor
@inv_router.get("/author", response_model=list[Author])
async def get_authors(session: Session = Depends(get_session)):
    return AuthorService(session).get_all_authors()

@inv_router.get("/author/{author_id}/books", response_model=list[Book])
async def get_books_by_author(author_id:int, session: Session = Depends(get_session)):
    return AuthorService(session).get_books_by_author(author_id)

@inv_router.delete("/author/{author_id}", response_model=Author)
async def delete_author_by_id(
    id: int, 
    _: bool = Depends(role_checker_factory(allowed_roles=[SELLER_ROLE])),
    session: Session = Depends(get_session)): 
    return AuthorService(session).delete_author_by_id(id) 

@inv_router.post("/author", response_model=AuthorResponse)
async def create_author(
    author: AuthorCreate, 
    _: bool = Depends(role_checker_factory(allowed_roles=[SELLER_ROLE])),
    session: Session = Depends(get_session)):
    return AuthorService(session).create(author)
#TODO: nicht möglich trotz authorization drauf zuzugreifen 

@inv_router.put("/author/{author_id}", response_model=Author)
async def update_author(
    id: int, 
    new_author: Author, 
    _: bool = Depends(role_checker_factory(allowed_roles=[SELLER_ROLE])),
    session: Session = Depends(get_session)):
    return AuthorService(session).update(id, new_author)


#Genre
@inv_router.get("/genre", response_model=list[Genre])
async def get_genres(session: Session = Depends(get_session)):
    return GenreService(session).get_all_genres()

@inv_router.get("/genre/{genre_id}/books", response_model= list[Book])
async def get_books_by_genre(genre_id: int, session: Session = Depends(get_session)):
    return GenreService(session).get_books_by_genre(genre_id)

@inv_router.delete("/genre/{genre_id}", response_model=Genre)
async def delete_genre_by_id(
    id: int,
    _: bool = Depends(role_checker_factory(allowed_roles=[SELLER_ROLE])),
    session: Session = Depends(get_session)): 
    return GenreService(session).delete_genre_by_id(id) 

@inv_router.post("/genre", response_model=GenreResponse)
async def create_genre(
    genre: GenreCreate, 
    _: bool = Depends(role_checker_factory(allowed_roles=[SELLER_ROLE])),
    session: Session = Depends(get_session)):
    return GenreService(session).create(genre)

@inv_router.put("/genre/{genre_id}", response_model=Genre)
async def update_genre(
    id: int, 
    new_genre: Genre, 
    _: bool = Depends(role_checker_factory(allowed_roles=[SELLER_ROLE])),
    session: Session = Depends(get_session)):
    return GenreService(session).update(id, new_genre)


#Publisher
@inv_router.get("/publisher", response_model=list[Publisher])
async def get_publishers(session: Session = Depends(get_session)):
    return PublisherService(session).get_all_publishers()

@inv_router.get("/publisher/{publisher_id}/books", response_model= list[Book])
async def get_books_by_publisher(publisher_id: int, session: Session = Depends(get_session)):
    return PublisherService(session).get_books_by_publisher(publisher_id)

@inv_router.delete("/publisher/{publisher_id}", response_model=Publisher)
async def delete_publisher_by_id(
    id: int, 
    _: bool = Depends(role_checker_factory(allowed_roles=[SELLER_ROLE])),
    session: Session = Depends(get_session)): 
    return PublisherService(session).delete_publisher_by_id(id) 

@inv_router.post("/publisher", response_model=PublisherResponse)
async def create_publisher(
    publisher: PublisherCreate, 
    _: bool = Depends(role_checker_factory(allowed_roles=[SELLER_ROLE])),
    session: Session = Depends(get_session)):
    return PublisherService(session).create(publisher)

@inv_router.put("/publisher/{publisher_id}", response_model=Publisher)
async def update_publisher(
    id: int, 
    new_publisher: Publisher, 
    _: bool = Depends(role_checker_factory(allowed_roles=[SELLER_ROLE])),
    session: Session = Depends(get_session)):
    return PublisherService(session).update(id, new_publisher)