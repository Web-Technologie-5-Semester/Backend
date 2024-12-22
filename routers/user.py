from functools import partial
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import Session
from db import get_session
from user.models import User, UserCreate
from user.service import UserService
from user.repositories import UserRepository
from db import session
from user.models import Token
import jwt
from jwt.exceptions import InvalidTokenError
from datetime import timedelta


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
ACCESS_TOKEN_EXP_MIN = 30

user_router = APIRouter()
user_serv = UserService(session)

# @user_router.get("/items/")
# async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
#     return {"token": token}

@user_router.post("/user")
async def create_user(user: UserCreate, session: Session = Depends(get_session)):
    return UserService(session).create_user(user)

@user_router.get("/users/me")
async def read_users_me(current_user: Annotated[User, Depends(UserService.get_current_active_user)]):
    return current_user


@user_router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    #user_pwd_hash = user_serv.get_password_hash(form_data.password)
    # user_data = user_serv.verify_password(form_data.password, user_pwd_hash)
    user = user_serv.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXP_MIN)
    access_token = user_serv.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

