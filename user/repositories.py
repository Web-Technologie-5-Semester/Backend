from sqlmodel import SQLModel, Session
from sqlalchemy import select, Engine
from .models import User


class UserRepository:
    engine :Engine = None
    session :Session = None

    def __init__(self, session: Session):
        self.session = session

    def get_all(self):
        users = self.session.exec(User).all()
        return users
    
    def get_user(self, email: str) -> User:
        stmt = select(User).where(User.email == email)
        result: User= self.session.exec(stmt).scalars().first()
        return result

    def create_user(self, email: str, password_hash: str):
        new_user = User(email=email, password_hash=password_hash)
        self.session.add(new_user)
        self.session.commit()
        self.session.refresh(new_user)
        return new_user
    
    def get_pwd(self, email: str):
        stmt = select(User).where(User.email == email)
        result = self.session.exec(stmt).scalars().first()
        return result