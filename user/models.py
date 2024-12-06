from pydantic import BaseModel
from sqlalchemy import Column, String
from sqlmodel import Field, Session, SQLModel, create_engine, select, Relationship



#User
class User(SQLModel, table = True):

    id: int | None = Field(default= None, primary_key= True)
    forename: str = Field()
    name: str = Field()
    email: str = Field()
    street: str = Field()
    house_number: int = Field()
    city: str = Field()
    district: str = Field()
    postal_code: int = Field()
    birthday: str = Field()
    password_hash: str = Field()
    role: str = Field(sa_column=Column(String, nullable=False))

    def __innit__(self, **kwargs):
        super().__init__(**kwargs)
        if not getattr(self, "role", None):
            self.role = "User"
   

class Customer(User):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.role = "Customer"
    

class Seller(User):

    IBAN: str = Field()
    sales_tax_id: int = Field()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.role = "Seller"


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None
