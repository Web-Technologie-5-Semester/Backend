from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, Depends, requests, status, FastAPI
import jwt
from jwt.exceptions import InvalidTokenError
from sqlmodel import Session
from user.repositories import UserRepository
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from user.models import User, Token, TokenData, UserCreate, UserUpdate
from db import session
from user.crypto import verify_password



SECRET_KEY = "97185efe61e4cdb4a5052f0a4fef3de03c3d946669d40a43cebcd6906d26f8a5"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXP_MIN = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class UserService():
    session :Session = None
    _self = None

    def __init__(self, session):
        self.session = session
        self.user_rep = UserRepository(session)
        self.user = User()
    
    def get_users(self, email: str):
        users :User = self.user_rep.get_user(email)
        if not users:
            return None
        return users
    
    def create_user(self, user: User):
        new_user = self.user_rep.add_user_if_not_exist(user)
        return new_user
    
    def delete_user(self, current_user: User):
        user: User = self.user_rep.get_user(current_user.email)
        if not user:
            return None
        else:
            self.user_rep.delete_user(user.email)
            return "User deleted"
        
    def update(self, new_user: UserUpdate, current_user: User):
        user = self.user_rep.update_user(new_user, current_user)
        return user
  
    def fake_decode_token(self, token):
        user = self.get_users(token)
        return user
    
    def get_current_user(self, token: Annotated[str, Depends(oauth2_scheme)]):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
            exp = payload.get("exp")
            if exp is None:
                raise credentials_exception
            exp_datetime = datetime.fromtimestamp(exp, tz=timezone.utc)
            if exp_datetime < datetime.now(tz=timezone.utc):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token ist abgelaufen",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            user = UserRepository(session).get_user(email= username)
            if user is None:
                raise credentials_exception
            return user
        except:
            raise credentials_exception
        
    