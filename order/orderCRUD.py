from pydantic import BaseModel
from typing import List
from datetime import date
from enum import Enum

class StatusEnum(str, Enum):
    SELECTED = "Selected"
    PAYED = "Payed"
    ORDERD = "Orderd"
    
    class Config:
        orm_mode = True


# ***********     Order    ***************

# CREATE
class OrderCreate(BaseModel):
    user_id: int

    shipping_address: str  
    billing_address: str

    status: StatusEnum = StatusEnum.SELECTED

    class Config:
        orm_mode = True
        
# READ
class OrderResponse(BaseModel):
    unique_order_id: int
    user_id: int
    created_at: date
    shipping_address: str  
    billing_address: str
    total_price: float
    
    status: StatusEnum
    items: List["OrderItemResponse"] 

    class Config:
        orm_mode = True
        
# UPDATE
class OrderUpdate(BaseModel):
    shipping_address: str  
    billing_address: str
    status: StatusEnum

    class Config:
        orm_mode = True
      

# ***********     OrderItems    ***************


# CREATE
class OrderItemCreate(BaseModel):
    
    unique_order_id: int
    product_id: str  
    quantity: int = 1
    price: float

    class Config:
        orm_mode = True

# READ
class OrderItemResponse(BaseModel):

    unique_order_id: int
    product_id: str
    quantity: int
    price: float

    class Config:
        orm_mode = True


# UPDATE
class OrderItemUpdate(BaseModel):
    quantity: int | None = None
    price: float | None = None

    class Config:
        orm_mode = True