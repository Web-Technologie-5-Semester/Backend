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
from passlib.context import CryptContext


SECRET_KEY = "97185efe61e4cdb4a5052f0a4fef3de03c3d946669d40a43cebcd6906d26f8a5"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXP_MIN = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



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
    
    def create_user(self, user: User):
        new_user = self.user_rep.check_user(user)
        return new_user
    
    #def create_seller(self, seller: Seller):

    
    def fake_decode_token(self, token):
        user = self.get_users(token)
        return user
    
    def get_password_hash(self, password):
        return pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)
    
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
        

    
    def get_current_active_user(self, current_user: Annotated[User, Depends(get_current_user)]):
        if current_user.disabled:
            raise HTTPException(status_code=400, detail="Inactive user")
        return current_user
    
    def authenticate_user(self, username: str, password: str):
        user = self.user_rep.get_user(username)
        if not user:
            return False 
        pwd_hash = self.get_password_hash(password)
        if not self.verify_password(password, pwd_hash):
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

#TODO: token sachen in extra file
#TODO: alle endpunkte sperren, bis auf neuen nutzer anlegen und gets öffentlich 
#TODO: Bild von Buch abspeichern