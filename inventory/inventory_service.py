#wenn neues buch angelegt, muss schauen ob autor schon da, wenn nicht, dann neuen anlegen, wenn ja dann zu autor repository 
from sqlalchemy.orm import Session
from sqlalchemy import select, Engine
from inventory.models import AuthorCreate, Book, Author, Genre, Publisher, BookResponse, AuthorResponse


class InventoryService():
    session :Session = None

    def __init__(self, session):
        self.session = session


    def new_author(self, author: AuthorCreate) -> Author:
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
            return new_author
        else:
            return result
        
    
    def new_genre(self, book:Book, genre: Genre):
        with Session(self.engine) as s:
            stmt = select(Author).where(genre.id == book.id_genre)
            result = s.exec(stmt).first()
            if result:
                return result
            else:
                genre_rep = GenreRepository()
                new_genre = genre_rep.create(genre)
                s.add(new_genre)
                s.commit()
                s.refresh(new_genre)
            return new_genre
        
    
    def new_publisher(self, book:Book, publisher: Publisher):
        with Session(self.engine) as s:
            stmt = select(Publisher).where(publisher.name == book.publisher)
            result = s.exec(stmt).first()
            if result:
                return result
            else:
                publisher_rep = PublisherRepository()
                new_publisher = publisher_rep.create(publisher)
                s.add(new_publisher)
                s.commit()
                s.refresh(new_publisher)
            return new_publisher        