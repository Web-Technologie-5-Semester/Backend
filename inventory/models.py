from pydantic import BaseModel
from sqlmodel import Field, Session, SQLModel, create_engine, select, Relationship
from datetime import date
from user.models import User


#Author 
class Author(SQLModel, table = True):

    id: int | None = Field(default= None, primary_key= True)
    name: str = Field()
    birthday: date = Field()

    books: list["Book"] = Relationship(back_populates="author")


class AuthorResponse(BaseModel):
    id: int 
    name: str
    birthday: date

    class Config:
        orm_mode = True


class AuthorCreate(BaseModel):
    name: str
    birthday: date

    class Config:
        orm_mode = True

class AuthorUpdate(BaseModel):
    id: int
    name: str | None = None
    birthday: date | None = None 



#Genre
class Genre(SQLModel, table = True):

    id: int | None = Field(default= None, primary_key= True)
    name: str

    books: list["Book"] = Relationship(back_populates="genre")


class GenreResponse(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class GenreCreate(BaseModel):
    name: str

    class Config:
        orm_mode = True

class GenreUpdate(BaseModel):
    id: int
    name: str | None = None



#Publisher
class Publisher(SQLModel, table = True):

    id: int | None = Field(default= None, primary_key= True)
    name: str

    books: list["Book"] = Relationship(back_populates="publisher")



class PublisherResponse(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class PublisherCreate(BaseModel):
    name: str

    class Config:
        orm_mode = True

class Update(BaseModel):
    id: int
    name: str | None = None



#Book
class Book(SQLModel, table = True):

    isbn: str | None = Field(default=None, primary_key=True)
    title: str = Field()
    
    release: date = Field()
    genre_id: int = Field(foreign_key="genre.id")
    description: str = Field()
    price: float = Field()
    age_recommendation: int = Field()
    publisher_id: int | None = Field(default=None, foreign_key="publisher.id")
    stock: int = Field()
    image: bytes= Field()

    author_id: int = Field(foreign_key="author.id")
    author: Author = Relationship(back_populates="books")
    genre: Genre | None = Relationship(back_populates="books")
    publisher: Publisher | None = Relationship(back_populates="books")
    user_id: int = Field(foreign_key="user.id")

class BookResponse(BaseModel):
    isbn: str
    title: str
    author: Author
    release: date
    genre: Genre
    description: str
    price: float
    age_recommendation: int
    publisher: Publisher
    stock: int
    image: bytes
    user_id: int
    
    class Config:
        orm_mode = True

class BookCreate(BaseModel):
    isbn: str
    title : str
    author_id : int
    release: date
    genre_id : int
    description : str
    price : float
    age_recommendation : int
    publisher_id : int
    stock: int
    image: bytes
    user_id: int

    class Config:
        orm_mode = True

class BookUpdate(BaseModel):
    isbn: str
    title : str | None = None
    author: AuthorResponse | None = None
    genre : str | None = None
    description : str | None = None
    price : str | None = None
    age_recommendation : int | None = None
    publisher : str | None = None
    image: bytes | None = None



