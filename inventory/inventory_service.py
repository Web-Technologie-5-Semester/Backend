#wenn neues buch angelegt, muss schauen ob autor schon da, wenn nicht, dann neuen anlegen, wenn ja dann zu autor repository 
from sqlalchemy.orm import Session
from sqlalchemy import select, Engine
from inventory.models import AuthorCreate, Book, BookCreate, Author, Genre, Publisher, GenreCreate
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
        author = self.book_rep.check_author(book.author)
        genre = self.book_rep.check_genre(book.genre)
        publisher = self.book_rep.check_publisher(book.publisher)
        new_book = self.book_rep.mapping_book(book, author, genre, publisher)
        return new_book
    
    def update(self, isbn: str, new_book: Book):
        book = self.book_rep.update(isbn, new_book)
        return book
    

class AuthorService():
    session :Session = None

    def __init__(self, session):
        self.session = session
        self.author_rep = AuthorRepository(session)

    def get_all_authors(self):
        return self.author_rep.get_all()
    
    def get_books_by_author(self, id: str):
        return self.author_rep.get_books_by_id(id)


class GenreService():
    session :Session = None

    def __init__(self, session):
        self.session = session
        self.genre_rep = GenreRepository(session)

    def get_all_genres(self):
        return self.genre_rep.get_all()
    
    def get_books_by_genre(self, id: str):
        return self.genre_rep.get_books_by_id(id)


class PublisherService():
    session :Session = None

    def __init__(self, session):
        self.session = session
        self.publisher_rep = PublisherRepository(session)

    def get_all_publishers(self):
        return self.publisher_rep.get_all()
    
    def get_books_by_publisher(self, id: str):
        return self.publisher_rep.get_books_by_id(id)


# class InventoryService():
#     session :Session = None

#     def __init__(self, session):
#         self.session = session


#     def new_author(self, author: AuthorCreate) -> Author:
#         stmt = select(Author).where(Author.name == author.name) #request zu viel, lieber id geben, abgleichen und dann mappen
#         result = self.session.exec(stmt).scalars().first()
#         if not result:
#             new_author = Author(
#                 name = author.name,
#                 birthday = author.birthday
#             )
#             self.session.add(new_author)
#             self.session.commit()
#             self.session.refresh(new_author)
#             return new_author
#         else:
#             return result
        
    
#     def new_genre(self, genre: GenreCreate) -> Genre:
#         stmt = select(Genre).where(Genre.genre == genre.genre)
#         result = self.session.exec(stmt).scalars().first()
#         if not result:
#             new_genre = Genre(
#                 genre = genre.genre
#             )
#             self.session.add(new_genre)
#             self.session.commit()
#             self.session.refresh(new_genre)
#             return new_genre
#         else:
#             return result
        
    
#     def new_publisher(self, publisher: Publisher) -> Publisher:
#         stmt = select(Publisher).where(Publisher.publisher == publisher.publisher)
#         result = self.session.exec(stmt).scalars().first()
#         if not result:
#             new_publisher = Publisher(
#                 publisher = publisher.publisher
#             )
#             self.session.add(new_publisher)
#             self.session.commit()
#             self.session.refresh(new_publisher)
#             return new_publisher
#         else:
#             return result    