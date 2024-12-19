from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, Depends, requests, status, FastAPI
from jwt.exceptions import InvalidTokenError
from sqlmodel import Session
from user.repositories import UserRepository
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from user.models import User


# SECRET_KEY = "97185efe61e4cdb4a5052f0a4fef3de03c3d946669d40a43cebcd6906d26f8a5"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXP_MIN = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class UserService():
    session :Session = None

    def __init__(self, session):
        self.session = session
        self.user_rep = UserRepository(session)
        self.user = User()
    

    def get_users(self, email: str):
        users :User = self.user_rep.get_users(email)
        if not users:
            return None
        return users
    
    def fake_decode_token(self, token):
        user = self.get_user(token)
        return user
    
    def fake_hash_pwd(self, password: str):
        return "fakehashed" + password
    
    async def get_current_user(self, token: Annotated[str, Depends(oauth2_scheme)]):
        user = self.fake_decode_token(token)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user

        
    # def get_pwd(self, email: str):
    #     user_pwd = self.user_rep.get_pwd(email)
    #     return user_pwd
    
    async def get_current_active_user(self, current_user: Annotated[User, Depends(get_current_user)]):
        if current_user.disabled:
            raise HTTPException(status_code=400, detail="Inactive user")
        return current_user
    
    # def verify_pwd(self, plain_password: str, hashed_password: str):
    #     return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())
        

