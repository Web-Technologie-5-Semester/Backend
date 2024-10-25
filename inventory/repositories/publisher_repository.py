from ..models.publisher import Publisher
from sqlmodel import SQLModel
from sqlalchemy import select, Engine
from sqlalchemy.orm import Session


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