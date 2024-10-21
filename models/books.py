from pydantic import BaseModel
from sqlmodel import Field, Session, SQLModel, create_engine, select
from datetime import date




class Book(SQLModel, table = True):

    isbn: int = Field(primary_key=True)
    title: str = Field()
    # id_author: int = Field(foreign_key="authors.id")
    release: date = Field()
    # genre: str = Field(foreign_key="genre.id")
    description: str = Field()
    price: float = Field()
    age_recommendation: int = Field()
    # publisher: str = Field(foreign_key="publisher.id")
    stock: int = Field()



    


class BookResponse(BaseModel):
    isbn: int
    title: str
    id_author: int
    release: date
    genre: str
    description: str
    price: float
    age_recommendation: int
    publisher: int
    stock: int

class BookCreate(BaseModel):
    title : str
    id_author : int 
    genre : str
    description : str
    price : str
    age_recommendation : int
    publisher : str

class BookUpdate(BaseModel):
    isbn: int
    title : str | None = None
    id_author : int | None = None
    genre : str | None = None
    description : str | None = None
    price : str | None = None
    age_recommendation : int | None = None
    publisher : str | None = None

# class BookDelete(BaseModel):
#     isbn : Integer