from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import Depends, HTTPException, status
from sqlalchemy import Engine
from sqlmodel import Session
from db import session
from user.service import UserService
import jwt
from jwt.exceptions import InvalidTokenError
from functools import partial
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from user.models import Token
from user.authentication import authenticate_user


SECRET_KEY = "97185efe61e4cdb4a5052f0a4fef3de03c3d946669d40a43cebcd6906d26f8a5"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXP_MIN = 30



       
class TokenData:
    session :Session = None

    def __init__(self):
        self.session = session
        self.user_serv = UserService(session)

    def login_for_access_token(self,
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    ) -> Token: 
        user = authenticate_user(form_data.username, form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXP_MIN)
        access_token = self.create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires)
        return Token(access_token=access_token, token_type="bearer")

    def create_access_token(self, data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt