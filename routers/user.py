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
from user.authentication import get_current_active_user


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
#    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
#) -> Token:
    # user = user_serv.authenticate_user(form_data.username, form_data.password)
    # if not user:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Incorrect username or password",
    #         headers={"WWW-Authenticate": "Bearer"},
    #     )
    # access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXP_MIN)
    # access_token = user_serv.create_access_token(
    #     data={"sub": user.email}, expires_delta=access_token_expires
    # return Token(access_token=access_token, token_type="bearer")

