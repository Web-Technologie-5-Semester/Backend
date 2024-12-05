from fastapi import APIRouter, Depends
from sqlmodel import Session
from db import get_session
from order.orderCRUD import OrderCreate, OrderItemCreate, OrderItemResponse, OrderItemUpdate, OrderResponse, OrderUpdate
from order.orderServices import OrderItemService, OrderService

router = APIRouter()

@router.post("/order", response_model=OrderResponse)
async def add_order(order: OrderCreate):
    return OrderService.create_a_new_order(order)

@router.get("/order/{unique_order_id}", response_model=OrderResponse)
async def get_order_by_id(unique_order_id: int):
    return OrderService.read_by_unique_order_id(unique_order_id)


@router.put("/order/{unique_order_id}", response_model=OrderResponse)
async def update_order(unique_order_id: int, order_update: OrderUpdate):
    return OrderService.update_an_order(unique_order_id, order_update)


@router.delete("/delete/order/{unique_order_id}")
async def delete_order(unique_order_id: int):
    return OrderService.delete_an_order(unique_order_id)


# OrderItem      
@router.post("/order/item", response_model=OrderItemResponse)
async def add_order_item(order_item: OrderItemCreate):
    return OrderItemService.create_an_order_item(order_item)
                                                  
@router.get("/order/item/{unique_order_item_id}", response_model=OrderItemResponse)
async def get_order_item(unique_order_item_id: int):
    return OrderItemService.read_by_unique_order_item_id(unique_order_item_id)
                                               
@router.put("/order/item/{unique_order_item_id}", response_model=OrderItemResponse)
async def update_order_item(unique_order_item_id: int, order_item_update: OrderItemUpdate):
    return OrderItemService.update_an_order_item(unique_order_item_id, order_item_update)
                                              
@router.delete("/order/item/{unique_order_item_id}")
async def delete_order_item(unique_order_item_id: int):
    return OrderItemService.delete_an_order_item(unique_order_item_id)