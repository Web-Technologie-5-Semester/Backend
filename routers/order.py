from fastapi import APIRouter, Depends
from sqlmodel import Session
from db import get_session
from order.orderCRUD import OrderCreate, OrderItemCreate, OrderItemResponse, OrderItemUpdate, OrderResponse, OrderUpdate
from order.orderServices import OrderItemService, OrderService

order_router = APIRouter()

@order_router.post("/order", response_model=OrderResponse)
async def add_order(order: OrderCreate, session: Session = Depends(get_session)):
    return OrderService(session).create_a_new_order(order)

@order_router.get("/order/{unique_order_id}", response_model=OrderResponse)
async def get_order_by_id(unique_order_id: int, session: Session = Depends(get_session)):
    return OrderService(session).read_by_unique_order_id(unique_order_id)


@order_router.put("/order/{unique_order_id}", response_model=OrderResponse)
async def update_order(unique_order_id: int, order_update: OrderUpdate, session: Session = Depends(get_session)):
    return OrderService(session).update_an_order(unique_order_id, order_update)


@order_router.delete("/delete/order/{unique_order_id}")
async def delete_order(unique_order_id: int, session: Session = Depends(get_session)):
    return OrderService(session).delete_an_order(unique_order_id)


# OrderItem      
@order_router.post("/order/item", response_model=OrderItemResponse)
async def add_order_item(order_item: OrderItemCreate, session: Session = Depends(get_session)):
    return OrderItemService(session).create_an_order_item(order_item)
                                                  
@order_router.get("/order/item/{unique_order_item_id}", response_model=OrderItemResponse)
async def get_order_item(unique_order_item_id: int, session: Session = Depends(get_session)):
    return OrderItemService(session).read_by_unique_order_item_id(unique_order_item_id)
                                               
@order_router.put("/order/item/{unique_order_item_id}", response_model=OrderItemResponse)
async def update_order_item(unique_order_item_id: int, order_item_update: OrderItemUpdate, session: Session = Depends(get_session)):
    return OrderItemService(session).update_an_order_item(unique_order_item_id, order_item_update)
                                              
@order_router.delete("/order/item/{unique_order_item_id}")
async def delete_order_item(unique_order_item_id: int, session: Session = Depends(get_session)):
    return OrderItemService(session).delete_an_order_item(unique_order_item_id)