from ..models.author import Author
from sqlmodel import SQLModel
from sqlalchemy import select, Engine
from sqlalchemy.orm import Session
import uuid

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