from pydantic import BaseModel
from typing import List
from datetime import date
from enum import Enum

class StatusEnum(str, Enum):
    SELECTED = "Selected"
    PAYED = "Payed"
    ORDERED = "Ordered"
    
    class Config:
        orm_mode = True


class OrderCreate(BaseModel):
    user_id: str

    class Config:
        orm_mode = True
        

class OrderResponse(BaseModel):
    unique_order_id: int
    user_id: str
    created_at: date
    shipping_address: str  
    billing_address: str
    total_price: float
    
    status: StatusEnum
    items: List["OrderItemResponse"] 

    class Config:
        orm_mode = True
        

class OrderUpdate(BaseModel):
    shipping_address: str  
    billing_address: str
    status: StatusEnum

    class Config:
        orm_mode = True
      



class OrderItemCreate(BaseModel):
    
    unique_order_id: int
    product_id: str  
    name: str
    image: str
    quantity: int = 1
    price: float

    class Config:
        orm_mode = True


class OrderItemResponse(BaseModel):

    unique_order_item_id: int
    product_id: str
    quantity: int
    price: float

    class Config:
        orm_mode = True



class OrderItemUpdate(BaseModel):
    quantity: int | None = None
    price: float | None = None

    class Config:
        orm_mode = True