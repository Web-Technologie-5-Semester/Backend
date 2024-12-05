# from datetime import datetime, timedelta, timezone
# from fastapi import HTTPException, Depends, requests, status, FastAPI
# import jwt
# from jose import JWTError
# from jwt.exceptions import InvalidTokenError
# from sqlmodel import Session
# from user.repositories import UserRepository
# from passlib.context import CryptContext
# from fastapi.security import OAuth2PasswordBearer
# from typing import Annotated
# from user.models import TokenData

# pwd_context= CryptContext(schemes=["bcrypt"], deprecated="auto")
# SECRET_KEY ="c8aab57e92c3ce594c8c6787dfce817bf0ab510cac10ebe509b4a84983fa3b34"
# ALGORITHM = "HS256"
# TOKEN_EXPIRE_MIN = 30

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# class UserService():
#     session :Session = None

#     def __init__(self, session):
#         self.session = session
#         self.user_rep = UserRepository(session)

    
#     def verify_pwd(self, plain_password, password_hash):
#         return pwd_context.verify(plain_password, password_hash)
    
#     def get_pwd_hash(self, password):
#         return pwd_context.hash(password)
    
#     def create_user(self, email: str, password: str):
#         password_hash = pwd_context.hash(password)
#         new_user = self.user_rep.create_user(email, password_hash)
#         return new_user
    
#     def authenticate_user(self, email: str, password:str):
#         user = self.user_rep.get_user(email)
#         if not user:
#             return False
#         if not self.verify_pwd(password, user.password_hash):
#             return False
#         return user
    
#     def create_access_token(self, data: dict, expires_delta: timedelta | None = None):
#         to_encode = data.copy()
#         if expires_delta:
#             expire = datetime.now(timezone.utc) + expires_delta
#         else:
#             expire = datetime.now(timezone.utc) + timedelta(minutes=15)
#         to_encode.update({"exp": expire})
#         encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#         return encoded_jwt
    
#     async def get_current_user(self, token: Annotated[str, Depends(oauth2_scheme)]):
#         credentials_exception = HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Could not validate credentials",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#         try:
#             payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#             username: str = payload.get("sub")
#             if username is None:
#                 raise credentials_exception
#             token_data = TokenData(username=username)
#         except InvalidTokenError:
#             raise credentials_exception
#         user = self.user_rep.get_user(username=token_data.username)
#         if user is None:
#             raise credentials_exception
#         return user

    
#     def token_validation(self, token: str):
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         if payload.get("exp") < datetime.now(timezone.utc).timestamp():
#             raise JWTError("Token expired")
#         return payload
        
#     def get_roles(self, payload: dict):
#         return payload.get("realm_access", {}).get("roles", [])
    
#     def check_role(self, payload: dict, required_role: str):
#         roles = self.get_roles(payload)
#         if required_role not in roles:
#             raise Exception("Access denied")
        
#     def refresh_token(self, refresh_token: str):
#         token_url = f"{self.url}/protocol/openid-connect/token"
#         response = requests.post(
#             token_url,
#             data={
#                 "grant_type": "refresh_token",
#                 "refresh_token": refresh_token,
#                 "client_id": self.client_id,
#                 "client_secret": "YOUR_CLIENT_SECRET",
#          },
#             headers={"Content-Type": "application/x-www-form-urlencoded"},
#         )
#         response.raise_for_status()
#         return response.json()  
    
#     def get_user_info(self, payload: dict):
#         return {
#             "user_id": payload.get("sub"),
#             "username": payload.get("preferred_username"),
#             "email": payload.get("email")
#         }
 