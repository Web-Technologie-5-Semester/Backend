from pydantic import BaseModel
from sqlalchemy import Column, String
from sqlmodel import Field, Session, SQLModel, create_engine, select, Relationship


class Role(SQLModel, table= True):

    id: int | None = Field(default= None, primary_key= True)
    role: str = Field()
    users: list["User"] = Relationship(back_populates="role")


class Seller(SQLModel, table=True):

    user_id: int = Field(primary_key=True, foreign_key="user.id")
    bank: str = Field()
    BIC: int = Field()
    banking_name: str = Field()
    IBAN: str = Field()
    sales_tax_id: int = Field()

    user: list["User"] = Relationship(back_populates="seller")

#User
class User(SQLModel, table = True):

    id: int | None = Field(default= None, primary_key= True)
    first_name: str = Field()
    name: str = Field()
    email: str = Field()
    street: str = Field()
    house_number: int = Field()
    city: str = Field()
    district: str = Field()
    postal_code: int = Field()
    birthday: str = Field()
    password_hash: str = Field()
    role_id: int = Field(foreign_key="role.id")

    role: Role = Relationship(back_populates="users")
    seller: Seller = Relationship(back_populates="user")



    


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None
