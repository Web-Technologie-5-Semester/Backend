from sqlmodel import SQLModel
from sqlalchemy import select, Engine
from sqlalchemy.orm import Session, joinedload, selectinload, subqueryload
import uuid
from .models import Author, AuthorResponse, Book, BookCreate, Genre, GenreResponse, Publisher, BookResponse, PublisherResponse
from .inventory_service import InventoryService


#Author
class AuthorRepository:

    def __init__(self, session: Session):
        self.session = session
        self.service = InventoryService(session)

    def get_all(self):
        #with Session(self.engine) as s:
        authors = self.session.query(Author).all()
        # stmt = select(Author)
        #     result = s.exec(stmt)
        #     authors = result.all()
        return authors
    
    def get_books_by_id(self, id_author: int):
        stmt = select(Book).where(Book.author_id == id_author)
        result = self.session.execute(stmt).scalars().all()
        return result
        #with Session(self.engine) as s:
        #return s.get(Author, id_author)
        
    def delete_by_id(self, id_author: int) -> None:
        self.session.delete(Author, id_author)
        self.session.commit()
    
    def create(self, author: Author):
        self.session.add(author)   
        self.session.commit()
        return author    

    def update(self, author: Author):
        self.create(author)
        return author
    


#Books
class BooksRepository:
    engine :Engine = None
    session :Session = None

    def __init__(self, session: Session):
        self.session = session

    
    def get_all(self):
        #with Session(self.engine) as s:
        books = self.session.query(Book).all()
            # stmt = select(Book)
            # result = s.execute(stmt)
            # books = result.all()
        return books
    
    def get_by_isbn(self, isbn: str):
        #with Session(self.engine) as s:
        stmt = select(Book).options(subqueryload(Book.author)).where(Book.isbn == isbn)
        #stmt = select(Book).where(Book.isbn == isbn)
        result = self.session.execute(stmt).scalars().first()

        return result #s.get(Book, isbn)
        
        
    # def get_by_author(self, author: str):
    #     with Session(self.engine) as s:
    #         return s.get(Book, author)
        
    def delete_by_isbn(self, isbn: str):
        #with Session(self.engine) as s:
        stmt = select(Book).where(Book.isbn == isbn) #.options(subqueryload(Book.author)).where(Book.isbn == isbn)
        result = self.session.execute(stmt).scalars().first()
        self.session.delete(result)
        self.session.commit()
        return result 
    
    def create(self, book: BookCreate):
        # stmt = select(Book).options(subqueryload(Book.author)).where(Book.isbn == book.isbn)
        # result = self.session.execute(stmt).first()
        author = InventoryService(self.session).new_author(book.author)
        genre = InventoryService(self.session).new_genre(book.genre)
        publisher = InventoryService(self.session).new_publisher(book.publisher)
        new_book = Book(
            isbn = book.isbn,
            title = book.title,
            author= author,
            release = book.release,
            genre = genre,
            description = book.description,
            price = book.price,
            age_recommendation = book.age_recommendation,
            publisher = publisher,
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
                genre = new_book.genre.genre
            ),
            description = new_book.description,
            price = new_book.price,
            age_recommendation = new_book.age_recommendation,
            publisher = PublisherResponse(
                id = new_book.publisher.id,
                publisher = new_book.publisher.publisher
            ),
            stock = new_book.stock
        )
        return book_resp   

    def update(self, isbn: str, new_book: Book):
        stmt = select(Book).options(subqueryload(Book.author)).where(Book.isbn == isbn)
        result :Book = self.session.execute(stmt).scalars().first()
        for key,value in dict(new_book).items():
            if key != "isbn":
                if hasattr(result, key):
                    setattr(result, key, value)
                else:
                    raise Exception(f'inexistent attribute {key}')
        self.session.add(result)
        self.session.commit()
        self.session.refresh(result)
        # self.create(result, s)
        # s.commit()
        return result
    
    


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
    session :Session = None

    def __init__(self, session):
        self.session = session

    def get_all(self):
        stmt = select(Genre)
        result = self.session.exec(stmt)
        genres = result.all()
        return genres
    
    def get_by_id(self, id_genre: int):
        return self.session.get(Genre, id_genre)
    
    def get_books_by_id(self, id_genre: int):
        stmt = select(Book).where(Book.genre_id == id_genre)
        result = self.session.execute(stmt).scalars().all()
        return result
        
    def delete_by_id(self, id_genre: int) -> None:
        self.session.delete(Genre, id_genre)
        self.session.commit()
    
    def create(self, genre: Genre):
        self.session.add(genre)   
        self.session.commit()
        return genre    

    def update(self, genre: Genre):
        self.create(genre)
        return genre
    


#Publisher
class PublisherRepository:
    session :Session = None

    def __init__(self, session):
        self.session = session

    def get_all(self):
        stmt = select(Publisher)
        result = self.session.exec(stmt)
        publisher = result.all()
        return publisher
    
    def get_by_id(self, id_publisher: int):
        return self.session.get(Publisher, id_publisher)
    
    def get_books_by_id(self, id_publisher: int):
        stmt = select(Book).where(Book.publisher_id == id_publisher)
        result = self.session.execute(stmt).scalars().all()
        return result
        
    def delete_by_id(self, id_publisher: int) -> None:
        self.session.delete(Publisher, id_publisher)
        self.session.commit()
    
    def create(self, publisher: Publisher):
        self.session.add(publisher)   
        self.session.commit()
        return publisher   

    def update(self, publisher: Publisher):
        self.create(publisher)
        return publisher