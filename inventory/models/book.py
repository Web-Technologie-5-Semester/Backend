from pydantic import BaseModel
from sqlmodel import Field, Session, SQLModel, create_engine, select, Relationship
from datetime import date
from .author import Author
from .genre import Genre
from .publisher import Publisher




class Book(SQLModel, table = True):

    isbn: int | None = Field(default=None, primary_key=True)
    title: str = Field()
    author_id: int | None = Field(default=None, foreign_key="author.id")
    release: date = Field()
    genre_id: int = Field(foreign_key="genre.id")
    description: str = Field()
    price: float = Field()
    age_recommendation: int = Field()
    publisher_id: int | None = Field(default=None, foreign_key="publisher.id")
    stock: int = Field()

    author: Author | None = Relationship(back_populates="books")
    genre: Genre | None = Relationship(back_populates="books")
    publisher: Publisher | None = Relationship(back_populates="books")


class BookResponse(BaseModel):
    isbn: int
    title: str
    author_id: int
    release: date
    genre: str
    description: str
    price: float
    age_recommendation: int
    publisher: int
    stock: int

class BookCreate(BaseModel):
    title : str
    author_id : int 
    genre : str
    description : str
    price : str
    age_recommendation : int
    publisher : str

class BookUpdate(BaseModel):
    isbn: int
    title : str | None = None
    author_id : int | None = None
    genre : str | None = None
    description : str | None = None
    price : str | None = None
    age_recommendation : int | None = None
    publisher : str | None = None

