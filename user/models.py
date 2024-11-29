from pydantic import BaseModel
from sqlmodel import Field, Session, SQLModel, create_engine, select, Relationship


#Role
class Role(SQLModel, table = True):

    id: int | None = Field(default=None, primary_key= True)
    role: str = Field()

    users: list["User"] = Relationship(back_populates="role")


#User
class User(SQLModel, table = True):

    id: int | None = Field(default= None, primary_key= True)
    forename: str = Field()
    name: str = Field()
    email: str = Field()
    residence: str = Field()
    postal_code: int = Field()
    street: str = Field()
    password_hash: str = Field()
    id_role: int = Field(foreign_key="role.id")
    sales_tax_id: int = Field(gt=0)

    role: Role = Relationship(back_populates="users")


class Token(BaseModel):
    access_token: str
    token_type: str