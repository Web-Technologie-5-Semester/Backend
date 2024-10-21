import uuid
from ..models.books import Book
from sqlmodel import SQLModel
from sqlalchemy import select, Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker
import threading



class BooksRepository:
    engine :Engine = None

    def __init__(self, engine):
        self.engine = Engine

    
    def get_all(self):
        with Session(self.engine) as s:
            stmt = select(Book)
            result = s.exec(stmt)
            books = result.all()
        return books
    
    def get_by_isbn(self, isbn: int):
        with Session(self.engine) as s:
            return s.get(Book, isbn)
        
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
class Singleton:
    instance = None 
    lock = threading.Lock() #nur ein Thread kann überprüfung durchführen

    def __new__(cls): #wird noch vor der innit aufgerufen, chekct, ob es wirklich keine Instanz gibt
        if cls.instance is None:
            with cls.lock:
                if cls.isinstance is None: # double checking, damit echt keine Instanz beim multithreading exitiert
                    cls.instance = super(Singleton, cls).__new__(cls)
                    cls._initialize_pool()
                return cls.instance
    
    def _initialize_pool(self):
        self.engine = create_engine('postgresql://postgres:admin@localhost:5431/db')
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def get_session(self): #sitzung um mit datenbank zu agieren 
        return self.SessionLocal()
    
#Dependency Injection 
def get_db():
    db_pool = Singleton()
    db = db_pool.get_session()
    try:
        yield db
    finally:
        db.close()