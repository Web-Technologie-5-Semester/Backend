from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, Depends, requests, status, FastAPI
import jwt
from jwt.exceptions import InvalidTokenError
from sqlmodel import Session
from user.repositories import UserRepository
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from user.models import User, Token, TokenData
from db import session


SECRET_KEY = "97185efe61e4cdb4a5052f0a4fef3de03c3d946669d40a43cebcd6906d26f8a5"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXP_MIN = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class UserService():
    session :Session = None

    def __init__(self, session):
        self.session = session
        self.user_rep = UserRepository(session)
        self.user = User()
    

    def get_user(self, email: str):
        users :User = self.user_rep.get_user(email)
        if not users:
            return None
        return users
    
    def fake_decode_token(self, token):
        user = self.get_users(token)
        return user
    
    def fake_hash_pwd(self, password: str):
        return "fakehashed" + password
    
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
            token_data = TokenData(username=username)
        except InvalidTokenError:
            raise credentials_exception
        user = UserRepository(session).get_user(email=token_data.username)
        if user is None:
            raise credentials_exception
        return user

    
    def get_current_active_user(self, current_user: Annotated[User, Depends(get_current_user)]):
        if current_user.disabled:
            raise HTTPException(status_code=400, detail="Inactive user")
        return current_user
    
    def authenticate_user(self, username: str, password: str):
        user = self.user_rep.get_user(username)
        if not user:
            return False 
        if user.password_hash != password:
            return False
        return user
    
    def create_access_token(self, data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
