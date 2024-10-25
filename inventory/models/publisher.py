from pydantic import BaseModel
from sqlmodel import Field, Session, SQLModel, create_engine, select, Relationship

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