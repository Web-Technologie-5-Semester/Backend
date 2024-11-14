#wenn neues buch angelegt, muss schauen ob autor schon da, wenn nicht, dann neuen anlegen, wenn ja dann zu autor repository 
from sqlalchemy.orm import Session
from sqlalchemy import select, Engine
from inventory.models import AuthorCreate, Book, BookCreate, Author, Genre, Publisher, GenreCreate, PublisherCreate
from inventory.repositories import BooksRepository, AuthorRepository, GenreRepository, PublisherRepository
# keine datenbankabfragen 




class BookService():
    session :Session = None

    def __init__(self, session):
        self.session = session
        self.book_rep = BooksRepository(session)

    
    def get_all_books(self):
        return self.book_rep.get_all()
    
    def get_book_by_isbn(self, isbn: str):
        return self.book_rep.get_by_isbn(isbn)
    
    def delete_book_by_isbn(self, isbn: str):
        return self.book_rep.delete_by_isbn(isbn)
    
    def create(self, book: BookCreate):
        #author = self.book_rep.check_author(book.author)
        #genre = self.book_rep.check_genre(book.genre)
        #publisher = self.book_rep.check_publisher(book.publisher)
        new_book = self.book_rep.mapping_book(book)
        return new_book
    
    def update(self, isbn: str, new_book: Book):
        book = self.book_rep.update(isbn, new_book)
        return book
    
    def search_book(self, word: str) -> list[Book]:
        books = self.book_rep.get_all_info()
        matching_books = []
        for book in books:
            if (word.lower() in book.title.lower()or
                word.lower() in book.author.name.lower() or
                word.lower() in book.genre.name.lower() or
                word.lower() in book.publisher.name.lower()):
                    matching_books.append(book)
        return matching_books
    

class AuthorService():
    session :Session = None

    def __init__(self, session):
        self.session = session
        self.author_rep = AuthorRepository(session)

    def get_all_authors(self):
        return self.author_rep.get_all()
    
    def get_books_by_author(self, id: str):
        return self.author_rep.get_books_by_id(id)
    
    def delete_author_by_id(self, id: int):
        return self.author_rep.delete_by_id(id)
    
    def create(self, author: AuthorCreate):
        new_author = self.author_rep.check_author(author)
        #new_author = self.author_rep.mapping_author(current_author)
        return new_author
    
    def update(self, id: int, new_author: Author):
        author = self.author_rep.update(id, new_author)
        return author


class GenreService():
    session :Session = None

    def __init__(self, session):
        self.session = session
        self.genre_rep = GenreRepository(session)

    def get_all_genres(self):
        return self.genre_rep.get_all()
    
    def get_books_by_genre(self, id: str):
        return self.genre_rep.get_books_by_id(id)
    
    def delete_genre_by_id(self, id: int):
        return self.genre_rep.delete_by_id(id)
    
    def create(self, genre: GenreCreate):
        old_genre = self.genre_rep.check_genre(genre.genre)
        new_genre = self.genre_rep.mapping_genre(old_genre)
        return new_genre
    
    def update(self, id: int, new_genre: Genre):
        genre = self.genre_rep.update(id, new_genre)
        return genre


class PublisherService():
    session :Session = None

    def __init__(self, session):
        self.session = session
        self.publisher_rep = PublisherRepository(session)

    def get_all_publishers(self):
        return self.publisher_rep.get_all()
    
    def get_books_by_publisher(self, id: str):
        return self.publisher_rep.get_books_by_id(id)
    
    def delete_publisher_by_id(self, id: int):
        return self.publisher_rep.delete_by_id(id)
    
    def create(self, publisher: PublisherCreate):
        publisher = self.publisher_rep.check_author(publisher.publisher)
        new_publisher = self.publisher_rep.mapping_publisher(publisher)
        return new_publisher
    
    def update(self, id: int, new_publisher: Publisher):
        publisher = self.publisher_rep.update(id, new_publisher)
        return publisher
    