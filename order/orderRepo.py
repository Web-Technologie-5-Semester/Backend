from sqlalchemy import select
from sqlalchemy.orm import Session
from .orderCRUD import OrderCreate, OrderItemCreate, OrderItemResponse, OrderItemUpdate, OrderResponse, OrderUpdate
from .orderModels import Order, Order_Item, StatusEnum




# ***********      Order     ************

class OrderRepository:
    def __init__(self, session: Session):
        self.session = session
        
    #   CREATE
    def create_new_order(self, order: OrderCreate):
        new_order = Order(
            user_id = order.user_id,
            status = StatusEnum.SELECTED
        )
        print(f"Debug: created_at = {new_order.created_at}")
        
        # Session aktualisieren
        self.session.add(new_order)
        self.session.commit()
        self.session.refresh(new_order)
        
        
        # order_response = self.create_order_response(new_order)
        order_response = new_order.unique_order_id
        
        return order_response
    
    
    
    def create_order_response(self, order: Order) -> OrderResponse:
        stmt = select(Order_Item).where(Order_Item.unique_order_id == order.unique_order_id)
        results = self.session.execute(stmt).scalars().all()

        items = [
            OrderItemResponse(
                unique_order_item_id=item.unique_order_item_id,
                product_id=item.product_id,
                quantity=item.quantity,
                price=item.price,
            )
            for item in results
        ]
        
        total_price = sum(item.price * item.quantity for item in items)


        response = OrderResponse(
            unique_order_id=order.unique_order_id,
            user_id=order.user_id,
            created_at=order.created_at,
            total_price=total_price,  
            status=order.status,
            items=items,
        )
        
        return response

    
    
    # READ
    def get_single_order_by_order_id(self, unique_order_id: int) -> OrderResponse:
        stmt = select(Order).where(Order.unique_order_id == unique_order_id)
        result = self.session.execute(stmt).scalars().first()
        
        if result:
            order_response = self.create_order_response(result)
            return order_response   
        else:
            raise Exception(f"Order with ID {unique_order_id} not found")    
        
        
    # READ
    def get_all_orders_by_user_id(self, user_id: str) -> list[OrderResponse]:
        stmt = select(Order).where(Order.user_id == user_id)
        results = self.session.execute(stmt).scalars().all()
        
        if results:
            order_responses = [self.create_order_response(order) for order in results]
            return order_responses
        else:
            raise Exception(f"No orders found for user with ID {user_id}")

        
        
        
    # UPDATE
    def update(self, unique_order_id: int, order_update: OrderUpdate) -> OrderResponse:
        stmt = select(Order).where(Order.unique_order_id == unique_order_id)
        order = self.session.execute(stmt).scalars().first()

        if not order:
            raise Exception(f"Order with ID {unique_order_id} not found")
        
        if order_update.status:
            order.status = order_update.status
        
        self.session.commit()
        self.session.refresh(order)

        order_response = self.create_order_response(order)
        
        return order_response
    
    
    # DELETE
    def delete_by_id(self, unique_order_id: int) -> None:
        stmt = select(Order).where(Order.unique_order_id == unique_order_id)
        result = self.session.execute(stmt).scalars().first()
        
        if result:
            self.session.delete(result)
            self.session.commit()
            return f"Order with ID {unique_order_id} has been successfully deleted."
        else:
            raise Exception(f"Order with ID {unique_order_id} not found")  
        
        
        
        
        
        
# ***********      OrderItem     ************
        
        
class OrderItemRepository:
    def __init__(self, session: Session):
        self.session = session

    
        # CREATE
    def add_bulk_of_items_to_order(self, order_items: list[OrderItemCreate]) -> OrderResponse:
        if not order_items:
            raise Exception("The order_items list cannot be empty")
        
        unique_order_id = order_items[0].unique_order_id
        existing_order = self.session.query(Order).filter(Order.unique_order_id == unique_order_id).first()

        if not existing_order:
            raise Exception(f"Order with ID {unique_order_id} not found")


        # Alle OrderItems hinzufügen
        for order_item in order_items:
            new_order_item = Order_Item(
                unique_order_id=unique_order_id,
                product_id=order_item.product_id,
                quantity=order_item.quantity,
                price=order_item.price
            )
            self.session.add(new_order_item)
            self.session.flush()  


        order_response = OrderRepository.get_single_order_by_order_id(unique_order_id)
        self.session.commit()

        return order_response


    # READ
    def get_by_id(self, unique_order_item_id: int) -> OrderItemResponse:
        stmt = select(Order_Item).where(Order_Item.unique_order_item_id == unique_order_item_id)
        result = self.session.execute(stmt).scalars().first()
        
        order_item_response = OrderItemResponse(
        unique_order_item_id = result.unique_order_item_id,
        product_id = result.product_id,
        quantity = result.quantity,
        price = result.price
        )
        return order_item_response


    # UPDATE
    def update(self, unique_order_item_id: int, order_item_update: OrderItemUpdate) -> OrderItemResponse:
        stmt = select(Order_Item).where(Order_Item.unique_order_item_id == unique_order_item_id)
        result = self.session.execute(stmt).scalars().first()

        if result:
            if order_item_update.quantity is not None:
                result.quantity = order_item_update.quantity
            if order_item_update.price is not None:
                result.price = order_item_update.price
            self.session.commit()
            self.session.refresh(result)

            order_item_response = OrderItemResponse(
                unique_order_item_id = result.unique_order_item_id,
                product_id = result.product_id,
                quantity = result.quantity,
                price = result.price
            )
          
            return order_item_response
    
        else:
          raise Exception(f"OrderItem with ID {unique_order_item_id} not found")
        
        
    # DELETE
    def delete_by_id(self, unique_order_item_id: int) -> None:
        stmt = select(Order_Item).where(Order_Item.unique_order_item_id == unique_order_item_id)
        result = self.session.execute(stmt).scalars().first()
        
        if result:
            self.session.delete(result)
            self.session.commit()
            return f"Order with ID {unique_order_item_id} has been successfully deleted."
        else:
          raise Exception(f"OrderItem with ID {unique_order_item_id} not found")
        


# Einlesen von Listen für ItemCreate

def convert_json_to_order_items(self, json_list: list[dict]) -> list[OrderItemCreate]:
    try:
        return [OrderItemCreate(**item) for item in json_list]
    except Exception:
        return []

       