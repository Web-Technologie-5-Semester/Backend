#wenn neues buch angelegt, muss schauen ob autor schon da, wenn nicht, dann neuen anlegen, wenn ja dann zu autor repository 
from inventory.repositories import AuthorRepository, GenreRepository, PublisherRepository
from sqlalchemy.orm import Session
from sqlalchemy import select, Engine
from inventory.models import Book, Author, Genre, Publisher


class InventoryService():


    # def get_author_name(self, isbn: int):
    #     with Session(self.engine) as s:
    #         book_stmt = select(Book).where(Book.isbn == isbn)
    #         book = s.query(book_stmt).first()
    #         author_stmt = select(Author).where(Author.id == book.author_id)
    #         result = s.query(author_stmt).first() 
    #         return result.author

    def new_author(self, book:Book, author: Author):
        with Session(self.engine) as s:
            stmt = select(Author).where(author.id == book.id_author)
            result = s.exec(stmt).first()
            if result:
                return result
            else:
                author_rep = AuthorRepository()
                new_author = author_rep.create(author)
                s.add(new_author)
                s.commit()
                s.refresh(new_author)
            return new_author
        
    
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