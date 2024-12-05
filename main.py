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
from inventory.exception import  ExistingException, ForbiddenException, NotFoundException
from fastapi.middleware.cors import CORSMiddleware
from starlette.types import ASGIApp
from starlette.middleware.base import BaseHTTPMiddleware
from db import engine


from routers.inventory import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(lifespan=lifespan)

# order_serv = OrderService(session)
# order_item_serv = OrderItemService(session)


app.include_router(router)

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

@app.post("/order", response_model=OrderResponse)
async def add_order(order: OrderCreate):
    return order_serv.create_a_new_order(order)

@app.get("/order/{unique_order_id}", response_model=OrderResponse)
async def get_order_by_id(unique_order_id: int):
    return order_serv.read_by_unique_order_id(unique_order_id)


@app.put("/order/{unique_order_id}", response_model=OrderResponse)
async def update_order(unique_order_id: int, order_update: OrderUpdate):
    return order_serv.update_an_order(unique_order_id, order_update)


@app.delete("/delete/order/{unique_order_id}")
async def delete_order(unique_order_id: int):
    return order_serv.delete_an_order(unique_order_id)


# OrderItem      
@app.post("/order/item", response_model=OrderItemResponse)
async def add_order_item(order_item: OrderItemCreate):
    return order_item_serv.create_an_order_item(order_item)
                                                  
@app.get("/order/item/{unique_order_item_id}", response_model=OrderItemResponse)
async def get_order_item(unique_order_item_id: int):
    return order_item_serv.read_by_unique_order_item_id(unique_order_item_id)
                                               
@app.put("/order/item/{unique_order_item_id}", response_model=OrderItemResponse)
async def update_order_item(unique_order_item_id: int, order_item_update: OrderItemUpdate):
    return order_item_serv.update_an_order_item(unique_order_item_id, order_item_update)
                                              
@app.delete("/order/item/{unique_order_item_id}")
async def delete_order_item(unique_order_item_id: int):
    return order_item_serv.delete_an_order_item(unique_order_item_id)



if __name__=="__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
