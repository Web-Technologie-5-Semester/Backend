from fastapi import Depends
from sqlmodel import SQLModel
from sqlalchemy import select, Engine
from sqlalchemy.orm import Session, joinedload, selectinload, subqueryload
import uuid

from db import get_session
from inventory.exception import ExistingException, NotFoundException
from .models import Author, AuthorResponse, AuthorCreate, Book, BookCreate, Genre, GenreResponse, GenreCreate, Publisher, PublisherCreate, BookResponse, PublisherResponse
#from .inventory_service import InventoryService
#nur datenbankabfragen 


#Author
class AuthorRepository:

    def __init__(self, session: Session):
        self.session = session


    def get_all(self):
        authors = self.session.query(Author).all()
        return authors
    
    def get_books_by_id(self, id_author: int):
        stmt = select(Book).where(Book.author_id == id_author)
        result = self.session.execute(stmt).scalars().all()
        if result == None:
            raise NotFoundException(id_author, Author.__name__)
        return result
        
    def delete_by_id(self, id_author: int) -> Author:
        stmt = select(Author).where(Author.id == id_author)
        result = self.session.execute(stmt).scalars().first()
        if result == None:
            raise NotFoundException(id_author, Author.__name__)
        
        self.session.delete(result) 
        self.session.commit()
        return result

    def check_author(self, author: AuthorCreate):
        stmt = select(Author).where(Author.name == author.name) 
        result = self.session.exec(stmt).scalars().first()
        if not result:
            new_author = Author(
                name = author.name,
                birthday = author.birthday
            )
            self.session.add(new_author)
            self.session.commit()
            self.session.refresh(new_author)

            author_resp = AuthorResponse(
            id = new_author.id,
            name = new_author.name,
            birthday = new_author.birthday
        )

            return author_resp
        else:
            return ExistingException(author.id, Author.__name__)
        #exception wenn autor schon existiert 
    
    def create(self, author: Author):
        self.session.add(author)   
        self.session.commit()
        return author    

    def update(self, id: int, new_author: Author):
        stmt = select(Author).where(Author.id == id)
        result :Author = self.session.execute(stmt).scalars().first()
        if result == None:
            raise NotFoundException(id, Author.__name__)
        for key,value in dict(new_author).items():
            if key != "id":
                if hasattr(result, key):
                    setattr(result, key, value)
                else:
                    raise Exception(f'inexistent attribute {key}')
        self.session.add(result)
        self.session.commit()
        self.session.refresh(result)
        return result
    


#Books
class BooksRepository:
    engine :Engine = None
    session :Session = None

    def __init__(self, session: Session):
        self.session = session

    
    def get_all(self):
        books = self.session.query(Book).all()
        return books
    
    def get_all_info(self):
        stmt = select(Book).options(subqueryload(Book.author), subqueryload(Book.genre), subqueryload(Book.publisher))
        result = self.session.execute(stmt).scalars().all()
        return result
    
    def get_by_isbn(self, isbn: str):
        stmt = select(Book).options(subqueryload(Book.author)).where(Book.isbn == isbn)
        result = self.session.execute(stmt).scalars().first()
        if result == None:
            raise NotFoundException(isbn, Book.__name__)
        return result 
        
    def delete_by_isbn(self, isbn: str):
        stmt = select(Book).where(Book.isbn == isbn) 
        result = self.session.execute(stmt).scalars().first()
        if result == None:
            raise NotFoundException(isbn, Book.__name__)
        self.session.delete(result)
        self.session.commit()
        return None   
    
    def mapping_book(self, book: Book):
        new_book = Book(
            isbn = book.isbn,
            title = book.title,
            author_id= book.author_id,
            release = book.release,
            genre_id = book.genre_id,
            description = book.description,
            price = book.price,
            age_recommendation = book.age_recommendation,
            publisher_id = book.publisher_id,
            stock = book.stock

        )

        self.session.add(new_book)
        self.session.commit()
        self.session.refresh(new_book)

        book_resp = BookResponse(
            isbn = new_book.isbn,
            title = new_book.title,
            author= AuthorResponse(
                id = new_book.author.id,
                name = new_book.author.name,
                birthday = new_book.author.birthday
            ),
            release = new_book.release,
            genre= GenreResponse(
                id = new_book.genre.id,
                name = new_book.genre.name
            ),
            description = new_book.description,
            price = new_book.price,
            age_recommendation = new_book.age_recommendation,
            publisher = PublisherResponse(
                id = new_book.publisher.id,
                name = new_book.publisher.name
            ),
            stock = new_book.stock
        )
        return book_resp

    def update(self, isbn: str, new_book: Book):
        stmt = select(Book).options(subqueryload(Book.author)).where(Book.isbn == isbn)
        result :Book = self.session.execute(stmt).scalars().first()
        if result == None:
            raise NotFoundException(isbn, Book.__name__)
        for key,value in dict(new_book).items():
            if key != "isbn":
                if hasattr(result, key):
                    setattr(result, key, value)
                else:
                    raise Exception(f'inexistent attribute {key}')
        self.session.add(result)
        self.session.commit()
        self.session.refresh(result)
        return result



#Genre
class GenreRepository:
    session :Session = None

    def __init__(self, session):
        self.session = session

    def get_all(self):
        genres = self.session.query(Genre).all()
        return genres
    
    def get_by_id(self, id_genre: int):
        stmt = select(Genre).where(Genre.id == id_genre)
        result = self.session.execute(stmt).scalars().all()
        if result == None:
            raise NotFoundException(id_genre, Genre.__name__)
        return result
    
    def get_books_by_id(self, id_genre: int):
        stmt = select(Book).where(Book.genre_id == id_genre)
        result = self.session.execute(stmt).scalars().all()
        if result == None:
            raise NotFoundException(id_genre, Genre.__name__)
        return result
        
    def delete_by_id(self, id_genre: int):
        stmt = select(Genre).where(Genre.id == id_genre)
        result = self.session.execute(stmt).scalars().first()
        if result == None:
            raise NotFoundException(id_genre, Genre.__name__)
        
        self.session.delete(result) 
        self.session.commit()
        return result

    def check_genre(self, genre: GenreCreate):
        stmt = select(Genre).where(Genre.name == genre.name) 
        result = self.session.exec(stmt).scalars().first()
        if not result:
            new_genre = Genre(
                name = genre.name
            )
            self.session.add(new_genre)
            self.session.commit()
            self.session.refresh(new_genre)

            genre_resp = GenreResponse(
            id = new_genre.id,
            name = new_genre.name
        )
            return genre_resp
        else:
            return ExistingException(genre.id, Genre.__name__)
    
    def create(self, genre: Genre):
        self.session.add(genre)   
        self.session.commit()
        return genre  

    def update(self, id: int, new_genre: Genre):
        stmt = select(Genre).where(Genre.id == id)
        result :Genre = self.session.execute(stmt).scalars().first()
        if result == None:
            raise NotFoundException(id_genre, Genre.__name__)
        for key,value in dict(new_genre).items():
            if key != "id":
                if hasattr(result, key):
                    setattr(result, key, value)
                else:
                    raise Exception(f'inexistent attribute {key}')
        self.session.add(result)
        self.session.commit()
        self.session.refresh(result)
        return result
    


#Publisher
class PublisherRepository:
    session :Session = None

    def __init__(self, session):
        self.session = session

    def get_all(self):
        publishers = self.session.query(Publisher).all()
        return publishers
    
    def get_by_id(self, id_publisher: int):
        stmt = select(Publisher).where(Publisher.id == id_publisher)
        result = self.session.execute(stmt).scalars().all()
        if result == None:
            raise NotFoundException(id_publisher, Publisher.__name__)
        return result
    
    def get_books_by_id(self, id_publisher: int):
        stmt = select(Book).where(Book.publisher_id == id_publisher)
        result = self.session.execute(stmt).scalars().all()
        if result == None:
            raise NotFoundException(id_publisher, Publisher.__name__)
        return result
        
    def delete_by_id(self, id_publisher: int) -> None:
        stmt = select(Publisher).where(Publisher.id == id_publisher)
        result = self.session.execute(stmt).scalars().first()
        if result == None:
            raise NotFoundException(id_publisher, Publisher.__name__)
        
        self.session.delete(result) 
        self.session.commit()
        return result
    
    def check_publisher(self, publisher: PublisherCreate):
        stmt = select(Publisher).where(Publisher.name == publisher.name) 
        result = self.session.exec(stmt).scalars().first()
        if not result:
            new_publisher = Publisher(
                name = publisher.name,
            )
            self.session.add(new_publisher)
            self.session.commit()
            self.session.refresh(new_publisher)

            publisher_resp = PublisherResponse(
            id = new_publisher.id,
            name = new_publisher.name
        )
            return publisher_resp
        else:
            return ExistingException(publisher.id, Publisher.__name__)
        
    def mapping_publisher(self, publisher: Publisher):
        new_publisher = Publisher(
            id = publisher.id,
            publisher = publisher.publisher
        )
        self.session.add(new_publisher)
        self.session.commit()
        self.session.refresh(new_publisher)

        publisher_resp = PublisherResponse(
            id = new_publisher.publisher.id,
            publisher = new_publisher.publisher.publisher
        )

        return publisher_resp
    
    def create(self, publisher: Publisher):
        self.session.add(publisher)   
        self.session.commit()
        return publisher

    def update(self, id: int, new_publisher: Publisher):
        stmt = select(Publisher).where(Publisher.id == id)
        result :Publisher = self.session.execute(stmt).scalars().first()
        if result == None:
            raise NotFoundException(id_publisher, Publisher.__name__)
        for key,value in dict(new_publisher).items():
            if key != "id":
                if hasattr(result, key):
                    setattr(result, key, value)
                else:
                    raise Exception(f'inexistent attribute {key}')
        self.session.add(result)
        self.session.commit()
        self.session.refresh(result)
        return result