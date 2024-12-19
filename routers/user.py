from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import Session
from db import get_session
from user.models import User
from user.service import UserService
from user.repositories import UserRepository
from db import session


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

user_router = APIRouter()
user_serv = UserService(session)

@user_router.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}

@user_router.get("/users/me")
async def read_users_me(
    current_user: Annotated[User, Depends(UserService.get_current_active_user)],
):
    return current_user


@user_router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict: User = user_serv.get_users(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    pwd = user_dict.password_hash
    if not pwd:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return {"access_token": user_dict.username, "token_type": "bearer"}
