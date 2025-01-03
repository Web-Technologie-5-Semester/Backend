from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select, Engine
from .orderRepo import OrderItemRepository, OrderRepository
from .orderCRUD import OrderCreate, OrderItemCreate, OrderItemResponse, OrderItemUpdate, OrderResponse, OrderUpdate
from .orderModels import Order, Order_Item, StatusEnum





class OrderService():
    session :Session = None
    
    def __init__(self, session):
        self.session = session
        self.orderRepo = OrderRepository(session)
        
    def create_a_new_order(self, order: OrderCreate) -> OrderResponse:
        return self.orderRepo.create_new_order(order)
    
    def read_by_unique_order_id(self, unique_order_id :int) -> OrderResponse:
        return self.orderRepo.get_single_order_by_order_id(unique_order_id)
    
    def read_by_unique_user_id(self, user_id :str) -> list[OrderResponse]:
        return self.orderRepo.get_all_orders_by_user_id(user_id)
    
    def update_an_order(self, unique_order_id :int, updated_order :OrderUpdate) -> OrderResponse:
        return self.orderRepo.update(unique_order_id, updated_order)
    
    def delete_an_order(self, unique_oder_id :int) -> None:
        return self.orderRepo.delete_by_id(unique_oder_id)
    
    
    
class OrderItemService():
    session :Session = None
    
    def __init__(self, session):
        self.session = session
        self.orderRepo = OrderItemRepository(session)
        
    def add_order_items(self, json_list: list[dict]) -> OrderResponse:
        order_items = self.orderRepo.convert_json_to_order_items(json_list)
        return self.orderRepo.add_bulk_of_items_to_order(order_items)
    
    def read_by_unique_order_item_id(self, unique_order_item_id :int) -> OrderItemResponse:
        return self.orderRepo.get_by_id(unique_order_item_id)
    
    def update_an_order_item(self, unique_order_item_id :int, updated_order_item :OrderItemUpdate) -> OrderItemResponse:
        return self.orderRepo.update(unique_order_item_id, updated_order_item)
    
    def delete_an_order_item(self, unique_oder_item_id :int) -> None:
        return self.orderRepo.delete_by_id(unique_oder_item_id)
    
#TODO: soll alles auf einmal geschickt werden? oder wie jetzt erst bestellung, dann jedes item einzeln
#TODO: Payment einrichten, stripe? Gute Doku
