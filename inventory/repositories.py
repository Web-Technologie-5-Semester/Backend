from sqlmodel import SQLModel
from sqlalchemy import select, Engine
from sqlalchemy.orm import Session, joinedload, selectinload, subqueryload
import uuid
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
        return result
        
    def delete_by_id(self, id_author: int) -> None:
        self.session.delete(Author, id_author)
        self.session.commit()

    def check_author(self, author: AuthorCreate) -> Author:
        stmt = select(Author).where(Author.name == author.name) #request zu viel, lieber id geben, abgleichen und dann mappen
        result = self.session.exec(stmt).scalars().first()
        if not result:
            new_author = Author(
                name = author.name,
                birthday = author.birthday
            )
            self.session.add(new_author)
            self.session.commit()
            self.session.refresh(new_author)
            return new_author
        else:
            return result
        
    def mapping_author(self,  author: Author):
        new_author = Author(
            id = author.id,
            name = author.name,
            birthday = author.birthday
        )
        self.session.add(new_author)
        self.session.commit()
        self.session.refresh(new_author)

        author_resp = AuthorResponse(
            id = new_author.author.id,
            name = new_author.author.name,
            birthday = new_author.author.birthday
        )

        return author_resp
    
    def create(self, author: Author):
        self.session.add(author)   
        self.session.commit()
        return author    

    def update(self, id: int, new_author: Author):
        stmt = select(Author).where(Author.id == id)
        result :Author = self.session.execute(stmt).scalars().first()
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
    
    def get_by_isbn(self, isbn: str):
        stmt = select(Book).options(subqueryload(Book.author)).where(Book.isbn == isbn)
        result = self.session.execute(stmt).scalars().first()
        return result 
        
    def delete_by_isbn(self, isbn: str):
        #with Session(self.engine) as s:
        stmt = select(Book).where(Book.isbn == isbn) #.options(subqueryload(Book.author)).where(Book.isbn == isbn)
        result = self.session.execute(stmt).scalars().first()
        self.session.delete(result)
        self.session.commit()
        return result   
    
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
    
    # def check_author(self, author: AuthorCreate) -> Author:
    #     stmt = select(Author).where(Author.name == author.name) #request zu viel, lieber id geben, abgleichen und dann mappen
    #     result = self.session.exec(stmt).scalars().first()
    #     if not result:
    #         new_author = Author(
    #             name = author.name,
    #             birthday = author.birthday
    #         )
    #         self.session.add(new_author)
    #         self.session.commit()
    #         self.session.refresh(new_author)
    #         return new_author
    #     else:
    #         return result
        
    def check_genre(self, genre: GenreCreate) -> Genre:
        stmt = select(Genre).where(Genre.genre == genre.genre)
        result = self.session.exec(stmt).scalars().first()
        if not result:
            new_genre = Genre(
                genre = genre.genre
            )
            self.session.add(new_genre)
            self.session.commit()
            self.session.refresh(new_genre)
            return new_genre
        else:
            return result
        
    def check_publisher(self, publisher: PublisherCreate) -> Publisher:
        stmt = select(Publisher).where(Publisher.publisher == publisher.publisher)
        result = self.session.exec(stmt).scalars().first()
        if not result:
            new_publisher = Publisher(
                publisher = publisher.publisher
            )
            self.session.add(new_publisher)
            self.session.commit()
            self.session.refresh(new_publisher)
            return new_publisher
        else:
            return result 


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
        #with Session(self.engine) as s:
        genres = self.session.query(Genre).all()
            # stmt = select(Book)
            # result = s.execute(stmt)
            # books = result.all()
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

    def check_genre(self, genre: GenreCreate) -> Genre:
        stmt = select(Genre).where(Genre.genre == genre.genre) 
        result = self.session.exec(stmt).scalars().first()
        if not result:
            new_genre = Genre(
                genre = genre.genre,
            )
            self.session.add(new_genre)
            self.session.commit()
            self.session.refresh(new_genre)
            return new_genre
        else:
            return result
        
    def mapping_genre(self,  genre: Genre):
        new_genre = Genre(
            id = genre.id,
            genre = genre.genre
        )
        self.session.add(new_genre)
        self.session.commit()
        self.session.refresh(new_genre)

        genre_resp = GenreResponse(
            id = new_genre.genre.id,
            genre = new_genre.genre.genre
        )

        return genre_resp
    
    def create(self, genre: Genre):
        self.session.add(genre)   
        self.session.commit()
        return genre  

    def update(self, id: int, new_genre: Genre):
        stmt = select(Genre).where(Genre.id == id)
        result :Genre = self.session.execute(stmt).scalars().first()
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
        #with Session(self.engine) as s:
        publishers = self.session.query(Publisher).all()
            # stmt = select(Book)
            # result = s.execute(stmt)
            # books = result.all()
        return publishers
    
    def get_by_id(self, id_publisher: int):
        return self.session.get(Publisher, id_publisher)
    
    def get_books_by_id(self, id_publisher: int):
        stmt = select(Book).where(Book.publisher_id == id_publisher)
        result = self.session.execute(stmt).scalars().all()
        return result
        
    def delete_by_id(self, id_publisher: int) -> None:
        self.session.delete(Publisher, id_publisher)
        self.session.commit()
    
    def check_publisher(self, publisher: PublisherCreate) -> Publisher:
        stmt = select(Publisher).where(Publisher.genre == publisher.publisher) 
        result = self.session.exec(stmt).scalars().first()
        if not result:
            new_publisher = Publisher(
                publisher = publisher.publisher,
            )
            self.session.add(new_publisher)
            self.session.commit()
            self.session.refresh(new_publisher)
            return new_publisher
        else:
            return result
        
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