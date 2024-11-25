from datetime import datetime, timedelta, timezone
import jwt
from sqlmodel import Session
from user.repositories import UserRepository
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

pwd_context= CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY ="39678b8be1e7114ddae8d8f33f926f3cb233ebc6b735f62580f9840c6809b831"
ALGORITHM = "HS256"


class UserService():
    session :Session = None

    def __init__(self, session):
        self.session = session
        self.user_rep = UserRepository(session)
        

    def verify_pwd(self, plain_password, password_hash):
        return pwd_context.verify(plain_password, password_hash)
    
    # def get_pwd_hash(self, password):
    #     return pwd_context.hash(password)

    def authenticate(self, email: str, password:str):
        user = self.user_rep.get_user(email)
        if not user:
            return False
        if not self.verify_pwd(password, user.password_hash):
            return False
        return user
    
    def create_user(self, email: str, password: str):
        password_hash = pwd_context.hash(password)
        new_user = self.user_rep.create_user(email, password_hash)
        return new_user
    
    def create_access_token(self, data: dict, expires: timedelta = None):
        to_encode = data.copy()
        if expires:
            expire = datetime.now(timezone.utc) + expires
        else: 
            expire = datetime.now(timezone.utc) +timedelta(minutes = 30)
        to_encode.update({"exp": expire})
        encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm= ALGORITHM)
        return encode_jwt
    