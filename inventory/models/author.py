from pydantic import BaseModel
from sqlmodel import Field, Session, SQLModel, create_engine, select, Relationship
from datetime import date


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