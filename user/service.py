# from datetime import datetime, timedelta, timezone
# import jwt
# from jose.exceptions import JWTError
# import requests
# from jwt.exceptions import InvalidTokenError
# from sqlmodel import Session
# from user.repositories import UserRepository
# from passlib.context import CryptContext
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

# pwd_context= CryptContext(schemes=["bcrypt"], deprecated="auto")
# SECRET_KEY ="c8aab57e92c3ce594c8c6787dfce817bf0ab510cac10ebe509b4a84983fa3b34"
# ALGORITHM = "RS256"
# TOKEN_EXPIRE_MIN = 30


# class UserService():
#     session :Session = None

#     def __init__(self, session):
#         self.session = session
#         self.user_rep = UserRepository(session)

#         self.url = "http://localhost:8000/token"
#         self.client_id = ""
#         self.jwks_url = f"{self.url}/protocol/openid-connect/certs"
#         self.jwks = self._fetch_jwks()

#     def _fetch_jwks(self):
#         response = requests.get(self.jwks_url)
#         response.raise_for_status()
#         return response.json()
    
#     def create_user(self, email: str, password: str):
#         password_hash = pwd_context.hash(password)
#         new_user = self.user_rep.create_user(email, password_hash)
#         return new_user
    
#     def token_validation(self, token: str):
#         try:
#             payload = jwt.decode(token, self.jwks, algorithms=[ALGORITHM], audience=self.client_id, issuer=self.url)
#             # email = payload.get("sub")
#             # if not email:
#             #     return False
#             return payload
#         except jwt.ExpiredSignatureError:
#             return "Token has expired"
#         except jwt.PyJWTError as e:
#             return f"Invalid token: {str(e)}"
        
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


    # def verify_pwd(self, plain_password, password_hash):
    #     return pwd_context.verify(plain_password, password_hash)
    
    # def get_pwd_hash(self, password):
    #     return pwd_context.hash(password)       

    # def authenticate(self, email: str, password:str):
    #     user = self.user_rep.get_user(email)
    #     if user.email != email:
    #         return False
    #     if not self.verify_pwd(password, user.password_hash):
    #         return False
    #     return user
    
    
    
    # def create_access_token(self, data: dict, expires: timedelta = None):
    #     to_encode = data.copy()
    #     if expires:
    #         expire = datetime.now(timezone.utc) + expires
    #     else: 
    #         expire = datetime.now(timezone.utc) +timedelta(minutes = 30)
    #     to_encode.update({"exp": expire})
    #     encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm= ALGORITHM)
    #     return encode_jwt
    