from pydantic import BaseModel
from sqlmodel import Field, Session, SQLModel, create_engine, select, Relationship
from datetime import date


#Author 
class Author(SQLModel, table = True):

    id: int | None = Field(default= None, primary_key= True)
    author: str = Field()
    firstName: str = Field()
    birthday: date = Field()

    books: list["Book"] = Relationship(back_populates="author")


class Response(BaseModel):
    id: int
    name: str
    firstName: str
    birthday: date

class Create(BaseModel):
    id: int
    name: str
    firstName: str
    birthday: date

class Update(BaseModel):
    id: int
    name: str | None = None
    firstName: str | None = None
    birthday: date | None = None 



#Genre
class Genre(SQLModel, table = True):

    id: int | None = Field(default= None, primary_key= True)
    genre: str

    books: list["Book"] = Relationship(back_populates="genre")


class Response(BaseModel):
    id: int
    genre: str

class Create(BaseModel):
    id: int
    genre: str

class Update(BaseModel):
    id: int
    genre: str | None = None



#Publisher
class Publisher(SQLModel, table = True):

    id: int | None = Field(default= None, primary_key= True)
    publisher: str

    books: list["Book"] = Relationship(back_populates="publisher")



class Response(BaseModel):
    id: int
    name: str

class Create(BaseModel):
    id: int
    name: str

class Update(BaseModel):
    id: int
    name: str | None = None



#Book
class Book(SQLModel, table = True):

    isbn: int | None = Field(default=None, primary_key=True)
    title: str = Field()
    
    release: date = Field()
    genre_id: int = Field(foreign_key="genre.id")
    description: str = Field()
    price: float = Field()
    age_recommendation: int = Field()
    publisher_id: int | None = Field(default=None, foreign_key="publisher.id")
    stock: int = Field()

    author_id: int = Field(foreign_key="author.id")
    author: Author = Relationship(back_populates="books")
    genre: Genre | None = Relationship(back_populates="books")
    publisher: Publisher | None = Relationship(back_populates="books")


class BookResponse(BaseModel):
    isbn: int
    title: str
    author_id: int
    release: date
    genre_id: int
    description: str
    price: float
    age_recommendation: int
    publisher_id: int 
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



