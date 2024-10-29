from sqlmodel import SQLModel
from sqlalchemy import select, Engine
from sqlalchemy.orm import Session
import uuid
from .models import Author, Book, Genre, Publisher


#Author
class AuthorRepository:
    engine :Engine = None

    def __init__(self, engine):
        self.engine = Engine

    def get_all(self):
        with Session(self.engine) as s:
            stmt = select(Author)
            result = s.exec(stmt)
            authors = result.all()
        return authors
    
    def get_by_id(self, id_author: uuid):
        with Session(self.engine) as s:
            return s.get(Author, id_author)
        
    def delete_by_id(self, id_author: uuid) -> None:
        with Session(self.engine) as s:
            s.delete(Author, id_author)
            s.commit()
    
    def create(self, author: Author):
        with Session(self.engine) as s:   
            s.add(author)   
            s.commit()
            return author    

    def update(self, author: Author):
        self.create(author)
        return author
    


#Books
class BooksRepository:
    engine :Engine = None

    def __init__(self, engine: Engine):
        self.engine = engine

    
    def get_all(self):
        with Session(self.engine) as s:
            books = s.query(Book).all()
            # stmt = select(Book)
            # result = s.execute(stmt)
            # books = result.all()
            return books
    
    def get_by_isbn(self, isbn: int):
        with Session(self.engine) as s:
            return s.get(Book, isbn)
        
    # def get_by_author(self, author: str):
    #     with Session(self.engine) as s:
    #         return s.get(Book, author)
        
    def delete_by_isbn(self, isbn: int) -> None:
        with Session(self.engine) as s:
            s.delete(Book, isbn)
            s.commit()
    
    def create(self, book: Book):
        with Session(self.engine) as s: 
            s.add(book)   
            s.commit()
            return book    

    def update(self, book: Book):
        self.create(book)
        return book


#Singleton
# class Singleton:
#     instance = None 
#     lock = threading.Lock() #nur ein Thread kann überprüfung durchführen

#     def __new__(cls): #wird noch vor der innit aufgerufen, chekct, ob es wirklich keine Instanz gibt
#         if cls.instance is None:
#             with cls.lock:
#                 if cls.isinstance is None: # double checking, damit echt keine Instanz beim multithreading exitiert
#                     cls.instance = super(Singleton, cls).__new__(cls)
#                     cls._initialize_pool()
#                 return cls.instance
    
#     def _initialize_pool(self):
#         self.engine = create_engine('postgresql://postgres:admin@localhost:5431/db')
#         self.session_local = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

#     def get_session(self): #sitzung um mit datenbank zu agieren 
#         return self.session_local()



#Genre
class GenreRepository:
    engine :Engine = None

    def __init__(self, engine):
        self.engine = Engine

    def get_all(self):
        with Session(self.engine) as s:
            stmt = select(Genre)
            result = s.exec(stmt)
            genres = result.all()
        return genres
    
    def get_by_id(self, id_genre: int):
        with Session(self.engine) as s:
            return s.get(Genre, id_genre)
        
    def delete_by_id(self, id_genre: int) -> None:
        with Session(self.engine) as s:
            s.delete(Genre, id_genre)
            s.commit()
    
    def create(self, genre: Genre):
        with Session(self.engine) as s:   
            s.add(genre)   
            s.commit()
            return genre    

    def update(self, genre: Genre):
        self.create(genre)
        return genre
    


#Publisher
class PublisherRepository:
    engine :Engine = None

    def __init__(self, engine):
        self.engine = Engine

    def get_all(self):
        with Session(self.engine) as s:
            stmt = select(Publisher)
            result = s.exec(stmt)
            publisher = result.all()
        return publisher
    
    def get_by_id(self, id_publisher: int):
        with Session(self.engine) as s:
            return s.get(Publisher, id_publisher)
        
    def delete_by_id(self, id_publisher: int) -> None:
        with Session(self.engine) as s:
            s.delete(Publisher, id_publisher)
            s.commit()
    
    def create(self, publisher: Publisher):
        with Session(self.engine) as s:   
            s.add(publisher)   
            s.commit()
            return publisher   

    def update(self, publisher: Publisher):
        self.create(publisher)
        return publisher