from sqlmodel import Field, SQLModel,  Relationship
from datetime import date
from typing import List, Optional
from enum import Enum
from pydantic import BaseModel
from .orderCRUD import StatusEnum




class Order(SQLModel, table=True):
    unique_order_id: int | None = Field(default=None, primary_key=True)
    
    user_id: str = Field()  
    created_at: date = Field(default=date.today)
    status: StatusEnum = Field()
    
    
    
    
class Order_Item(SQLModel, table=True):
    unique_order_item_id: int | None = Field(default=None, primary_key=True)

    unique_order_id: int = Field(foreign_key="order.unique_order_id")
    product_id: str = Field()
    name: str = Field()
    image: str = Field(default = None)
    quantity: int = Field(default=1)
    price: float = Field()





    
    
    
