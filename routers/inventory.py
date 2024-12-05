from fastapi import APIRouter, Depends
from sqlmodel import Session
from inventory.models import Author, AuthorCreate, AuthorResponse, Book, BookCreate, BookResponse, Genre, GenreCreate, GenreResponse, Publisher, PublisherCreate, PublisherResponse
from inventory.inventory_service import BookService, AuthorService, GenreService, PublisherService
from db import get_session

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

@inv_router.delete("/book/{isbn}", response_model=Book)
async def delete_book_by_isbn(isbn: str, session: Session = Depends(get_session)): 
    return BookService(session).delete_book_by_isbn(isbn)

@inv_router.post("/book", response_model=BookResponse)
async def create_book(book: BookCreate, session: Session = Depends(get_session)):
    return BookService(session).create(book)
                                 
@inv_router.put("/book/{isbn}", response_model=Book)
async def update_book(isbn: str, new_book :Book, session: Session = Depends(get_session)):
    return BookService(session).update(isbn, new_book)
                                 
#such endpunkt
@inv_router.post("/search", response_model=list[Book])
async def search(word: str, session: Session = Depends(get_session)):
    return BookService(session).search_book(word)


#Auhtor
@inv_router.get("/author", response_model=list[Author])
async def get_authors(session: Session = Depends(get_session)):
    return AuthorService(session).get_all_authors()

@inv_router.get("/author/{author_id}/books", response_model=list[Book])
async def get_books_by_author(author_id:int, session: Session = Depends(get_session)):
    return AuthorService(session).get_books_by_author(author_id)

@inv_router.delete("/author/{author_id}", response_model=Author)
async def delete_author_by_id(id: int, session: Session = Depends(get_session)): 
    return AuthorService(session).delete_author_by_id(id) 

@inv_router.post("/author", response_model=AuthorResponse)
async def create_author(author: AuthorCreate, session: Session = Depends(get_session)):
    return AuthorService(session).create(author)

@inv_router.put("/author/{author_id}", response_model=Author)
async def update_author(id: int, new_author: Author, session: Session = Depends(get_session)):
    return AuthorService(session).update(id, new_author)


#Genre
@inv_router.get("/genre", response_model=list[Genre])
async def get_genres(session: Session = Depends(get_session)):
    return GenreService(session).get_all_genres()

@inv_router.get("/genre/{genre_id}/books", response_model= list[Book])
async def get_books_by_genre(genre_id: int, session: Session = Depends(get_session)):
    return GenreService(session).get_books_by_genre(genre_id)

@inv_router.delete("/genre/{genre_id}", response_model=Genre)
async def delete_genre_by_id(id: int, session: Session = Depends(get_session)): 
    return GenreService(session).delete_genre_by_id(id) 

@inv_router.post("/genre", response_model=GenreResponse)
async def create_genre(genre: GenreCreate, session: Session = Depends(get_session)):
    return GenreService(session).create(genre)

@inv_router.put("/genre/{genre_id}", response_model=Genre)
async def update_genre(id: int, new_genre: Genre, session: Session = Depends(get_session)):
    return GenreService(session).update(id, new_genre)


#Publisher
@inv_router.get("/publisher", response_model=list[Publisher])
async def get_publishers(session: Session = Depends(get_session)):
    return PublisherService(session).get_all_publishers()

@inv_router.get("/publisher/{publisher_id}/books", response_model= list[Book])
async def get_books_by_publisher(publisher_id: int, session: Session = Depends(get_session)):
    return PublisherService(session).get_books_by_publisher(publisher_id)

@inv_router.delete("/publisher/{publisher_id}", response_model=Publisher)
async def delete_publisher_by_id(id: int, session: Session = Depends(get_session)): 
    return PublisherService(session).delete_publisher_by_id(id) 

@inv_router.post("/publisher", response_model=PublisherResponse)
async def create_publisher(publisher: PublisherCreate, session: Session = Depends(get_session)):
    return PublisherService(session).create(publisher)

@inv_router.put("/publisher/{publisher_id}", response_model=Publisher)
async def update_publisher(id: int, new_publisher: Publisher, session: Session = Depends(get_session)):
    return PublisherService(session).update(id, new_publisher)