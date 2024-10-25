from ..models.genre import Genre
from sqlmodel import SQLModel
from sqlalchemy import select, Engine
from sqlalchemy.orm import Session


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