from typing import Annotated
from fastapi import Depends
from sqlalchemy import create_engine
from sqlmodel import Session


sql_url = "postgresql://postgres:admin@localhost:5431/db"

connect_args = {"check_same_thread": False}
engine = create_engine(sql_url, echo=True)
session = Session(engine)


def get_session():
    with Session(engine) as session:
        yield session

#SessionDep = Annotated[Session, Depends(get_session)]