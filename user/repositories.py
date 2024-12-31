from datetime import datetime, timezone
import jwt
from sqlmodel import SQLModel, Session
from sqlalchemy import select, Engine

from user.crypto import get_password_hash

from .models import User, UserResponse, UserCreate
from .exception import ExistingException


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
    
    def add_user_if_not_exist(self, user: UserCreate):
        stmt = select(User).where(User.email == user.email) 
        result = self.session.exec(stmt).scalars().first()
        if not result:
            new_user = User(
                first_name = user.first_name,
                name = user.name,
                email = user.email,
                street= user.street,
                house_number= user.house_number,
                city= user.city,
                district= user.district,
                postal_code= user.postal_code,
                birthday = user.birthday,
                password_hash = get_password_hash(user.password),
                role_id = user.role_id,
                bank = user.bank,
                BIC = user.BIC,
                banking_name= user.banking_name,
                IBAN = user.IBAN,
                sales_tax_id= user.sales_tax_id 
            )
            self.session.add(new_user)
            self.session.commit()
            self.session.refresh(new_user)

            user_resp = UserResponse(
            id = new_user.id,
            first_name = new_user.first_name,
            name = new_user.name,
            email = new_user.email,
            street= new_user.street,
            house_number= new_user.house_number,
            city= new_user.city,
            district= new_user.district,
            postal_code= new_user.postal_code,
            birthday = new_user.birthday,
            role_id = new_user.role_id,
            bank = new_user.bank,
            BIC = new_user.BIC,
            banking_name= new_user.banking_name,
            IBAN = new_user.IBAN,
            sales_tax_id= new_user.sales_tax_id 
        )

            return user_resp
        else:
            return ExistingException(user.id, User.__name__)

