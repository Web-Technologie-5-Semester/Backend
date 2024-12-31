from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import Session
from db import get_session
from user.models import User, UserCreate
from user.service import UserService
from db import session
from user.token import TokenData
from datetime import timedelta
from user.authentication import get_current_active_user, logout_user


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


user_router = APIRouter()
user_serv = UserService(session)

@user_router.post("/user")
async def create_user(user: UserCreate, session: Session = Depends(get_session)):
    return UserService(session).create_user(user)

@user_router.get("/users/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user

@user_router.post("/token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    return TokenData().login_for_access_token(form_data)

@user_router.delete("/user")
async def delete_user(current_user: Annotated[User, Depends(get_current_active_user)]):
    return user_serv.delete_user(current_user)

