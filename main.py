from typing import Annotated
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn
from passlib.context import CryptContext
from sqlmodel import create_engine, Session, SQLModel
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, Request, status
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
from routers.user import user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(lifespan=lifespan)




app.include_router(inv_router)
app.include_router(order_router)
app.include_router(user_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


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
