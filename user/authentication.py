from typing import Annotated
from fastapi import Depends, HTTPException
from passlib.context import CryptContext
from sqlmodel import Session
from db import session
from user.models import User
from user.repositories import UserRepository
from user.service import UserService

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
user_rep = UserRepository(session)
user_serv = UserService(session)

# def init(session: Session):
#     user_rep = UserRepository(session)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def get_current_active_user(current_user: Annotated[User, Depends(user_serv.get_current_user)]):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def authenticate_user(username: str, password: str) -> User | None:
    user = user_rep.get_user(username)
    if not user:
        return None 
    if not verify_password(password, user.password_hash):
        return None
    return user

def logout_user(token: str):
    valid_token = user_rep.check_valid_token(token)
    if token in valid_token:
        valid_token.discard(token)
        return "Logout succsessful"
    else:
        raise HTTPException(status_code=400, detail="Invalid token")

