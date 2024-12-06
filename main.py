from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn
from passlib.context import CryptContext
from sqlmodel import create_engine, Session, SQLModel
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from order.orderCRUD import OrderCreate, OrderItemCreate, OrderItemResponse, OrderItemUpdate, OrderResponse, OrderUpdate
from order.orderServices import OrderItemService, OrderService
from user.models import User
from inventory.exception import  ExistingException, ForbiddenException, NotFoundException
from fastapi.middleware.cors import CORSMiddleware
from starlette.types import ASGIApp
from starlette.middleware.base import BaseHTTPMiddleware
from db import engine
from routers.inventory import inv_router
from routers.order import order_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(lifespan=lifespan)

# order_serv = OrderService(session)
# order_item_serv = OrderItemService(session)


app.include_router(inv_router)
app.include_router(order_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# class AuthMiddleware(BaseHTTPMiddleware):
#     def __init__(self, app: ASGIApp, token_validator: Callable):
#         super().__init__(app)
#         self.token_validator = token_validator

#     async def dispatch(self, request: Request, call_next):
#         if request.url.path == "/token" or request.url.path.startswith("/docs") or request.url.path.startswith("/openapi.json"):
#             return await call_next(request)

#         # Token aus den Headers extrahieren
#         authorization: str = request.headers.get("Authorization")
#         if not authorization or not authorization.startswith("Bearer "):
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="Authorization header missing or invalid",
#                 headers={"WWW-Authenticate": "Bearer"},
#             )

#         token = authorization.split(" ")[1]
#         try:
#             payload = self.token_validator(token)
#             request.state.user = payload  # Benutzerinformationen verfügbar machen
#         except JWTError:
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="Invalid or expired token",
#                 headers={"WWW-Authenticate": "Bearer"},
#             )

#         return await call_next(request)


# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# #Log in
# @app.post("/token")
# async def login_for_access_token(
#     form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
# ) -> Token:
#     user = user_service.authenticate_user(form_data.username, form_data.password)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token_expires = timedelta(minutes=user_service.ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = user_service.create_access_token(
#         data={"sub": user.username}, expires_delta=access_token_expires
#     )
#     return Token(access_token=access_token, token_type="bearer")



#Exception###############################################################
@app.exception_handler(NotFoundException)
async def not_found_handler(request: Request, exc: NotFoundException):
    return JSONResponse(
        status_code=404,
        content= {"message": exc.to_string()}
    )

@app.exception_handler(ForbiddenException)
async def forbidden_handler(request: Request, exc: ForbiddenException):
    return JSONResponse(
        status_code= 403,
        content= {"message": exc.to_string()}
    )

@app.exception_handler(ExistingException)
async def forbidden_handler(request: Request, exc: ExistingException):
    return JSONResponse(
        status_code= 409,
        content= {"message": exc.to_string()}
    )
####################################################################



# Order





if __name__=="__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
