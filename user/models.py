from pydantic import BaseModel
from sqlalchemy import Column, String
from sqlmodel import Field, Session, SQLModel, create_engine, select, Relationship


class Role(SQLModel, table= True):

    id: int | None = Field(default= None, primary_key= True)
    role: str = Field()
    users: list["User"] = Relationship(back_populates="role")

class User(SQLModel, table = True):

    id: int | None = Field(default= None, primary_key= True)
    first_name: str = Field()
    name: str = Field()
    email: str = Field()
    phone_number: str = Field()
    street: str = Field()
    house_number: int = Field()
    city: str = Field()
    district: str = Field()
    postal_code: int = Field()
    birthday: str = Field()
    password_hash: str = Field()
    role_id: int = Field(foreign_key="role.id")
    disabled: bool = Field(default=False)


    bank: str | None = Field()  
    BIC: str | None = Field()
    banking_name: str | None = Field()
    IBAN: str | None = Field()
    sales_tax_id: str | None = Field()

    role: Role = Relationship(back_populates="users")
    

class UserResponse(BaseModel):
    first_name: str 
    name: str 
    email: str 
    phone_number: str
    street: str 
    house_number: int 
    city: str 
    district: str 
    postal_code: int 
    birthday: str 

    bank: str | None = None 
    BIC: str | None = None
    banking_name: str | None = None
    IBAN: str | None = None
    sales_tax_id: str | None = None

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    first_name: str 
    name: str 
    email: str
    phone_number: str
    street: str
    house_number: int 
    city: str 
    district: str 
    postal_code: int 
    birthday: str 
    password: str
    role_id: int 

    bank: str | None = None 
    BIC: str | None = None
    banking_name: str | None = None
    IBAN: str | None = None
    sales_tax_id: str | None = None


    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    first_name: str | None = None
    name: str | None = None
    email: str | None = None
    phone_number: str | None = None
    street: str | None = None
    house_number: int | None = None
    city: str | None = None
    district: str | None = None
    postal_code: int | None = None
    birthday: str | None = None

    bank: str | None = None 
    BIC: str | None = None
    banking_name: str | None = None
    IBAN: str | None = None
    sales_tax_id: str | None = None

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

