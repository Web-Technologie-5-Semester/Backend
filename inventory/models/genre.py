from pydantic import BaseModel
from sqlmodel import Field, Session, SQLModel, create_engine, select, Relationship

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