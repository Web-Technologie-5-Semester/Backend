from sqlmodel import Field, SQLModel,  Relationship
from datetime import date
from typing import List, Optional
from enum import Enum
from pydantic import BaseModel
from .orderCRUD import StatusEnum




class Order(SQLModel, table=True):
    unique_order_id: int | None = Field(default=None, primary_key=True)
    
    # user_id: int = Field(foreign_key="user.id")  
    user_id: str = Field()  
    
    created_at: date = Field(default=date.today)
    status: StatusEnum = Field()
    
    items: List["Order_Item"] = Relationship(back_populates="order")  
    

    
class Order_Item(SQLModel, table=True):
    # wird beim erstellen vergeben
    unique_order_item_id: int | None = Field(default=None, primary_key=True)
    
    
    
    # Wichtig, kommt als response von order_create zurück
    unique_order_id: int = Field(foreign_key="order.unique_order_id")
    
    # sollten in der liste stehen 
    product_id: str = Field(foreign_key="book.isbn")  
    quantity: int = Field(default=1)
    price: float = Field()
    
    
    # unwichtig
    order: Order = Relationship(back_populates="items")  







#TODO: Order create gehört zu models 


    
    
    
    
