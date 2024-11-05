#wenn neues buch angelegt, muss schauen ob autor schon da, wenn nicht, dann neuen anlegen, wenn ja dann zu autor repository 
from sqlalchemy.orm import Session
from sqlalchemy import select, Engine
from inventory.models import AuthorCreate, Book, Author, Genre, Publisher, GenreCreate


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
        
    
    def new_genre(self, genre: GenreCreate) -> Genre:
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
        
    
    def new_publisher(self, publisher: Publisher) -> Publisher:
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