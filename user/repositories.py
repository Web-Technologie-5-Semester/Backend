from sqlmodel import SQLModel
from sqlalchemy import select, Engine
from .models import User


class UserRepository:

    def __init__(self, session: Session):
        self.session = session

    def get_all(self):
        users = self.session.query(User).all()
        return users