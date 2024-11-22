from sqlalchemy import select
from sqlalchemy.orm import Session
from .orderCRUD import OrderCreate, OrderItemCreate, OrderItemResponse, OrderItemUpdate, OrderResponse, OrderUpdate
from .orderModels import Order, Order_Item, StatusEnum




# ***********      Order     ************

class OrderRepository:
    def __init__(self, session: Session):
        self.session = session
        
    #   CREATE
    def create_new_order(self, order: OrderCreate) -> OrderResponse:
        new_order = Order(
            
            user_id = order.user_id,
            shipping_address = order.shipping_address, 
            billing_address = order.billing_address,
            status = order.status
        )
        
        
        # Session aktualisieren
        self.session.add(new_order)
        self.session.commit()
        self.session.refresh(new_order)
        
        
        order_response = self.create_order_response(new_order)

        return order_response
    
    
    
    def create_order_response(self, order: Order) -> OrderResponse:

        items = [
            OrderItemResponse(
                unique_order_item_id=item.unique_order_item_id,
                product_id=item.product_id,
                quantity=item.quantity,
                price=item.price,
            )
            for item in order.items
        ]
        
        total_price = sum(item.price * item.quantity for item in order.items)


        response = OrderResponse(
            unique_order_id=order.unique_order_id,
            user_id=order.user_id,
            created_at=order.created_at,
            shipping_address=order.shipping_address,
            billing_address=order.billing_address,
            total_price=total_price,  
            status=order.status,
            items=items,
        )
        
        return response

    
    
    # READ
    def get_by_order_id(self, unique_order_id: int) -> OrderResponse:
        stmt = select(Order).where(Order.unique_order_id == unique_order_id)
        result = self.session.execute(stmt).scalars().first()
        
        if result:
            order_response = self.create_order_response(result)
            return order_response   
        else:
            raise Exception(f"Order with ID {unique_order_id} not found")    
        
        # UPDATE
    def update(self, unique_order_id: int, order_update: OrderUpdate) -> OrderResponse:
        stmt = select(Order).where(Order.unique_order_id == unique_order_id)
        order = self.session.execute(stmt).scalars().first()

        if not order:
            raise Exception(f"Order with ID {unique_order_id} not found")
        
        if order_update.shipping_address:
            order.shipping_address = order_update.shipping_address
        if order_update.billing_address:
            order.billing_address = order_update.billing_address
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
    def create(self, order_item: OrderItemCreate) -> OrderItemResponse:
        existing_order = self.session.query(Order).filter(Order.unique_order_id == order_item.unique_order_id).first()

        if not existing_order:
            order_that_was_created = OrderRepository(self.session).create(OrderCreate)
            order_item.unique_order_id = order_that_was_created.unique_order_id
            
        new_order_item = Order_Item(
            unique_order_id = order_item.unique_order_id,
            product_id = order_item.product_id,
            quantity = order_item.quantity,
            price = order_item.price
        )
        self.session.add(new_order_item)
        self.session.commit()
        self.session.refresh(new_order_item)
        
        
        order_item_response = OrderItemResponse(
        product_id=new_order_item.product_id,
        quantity=new_order_item.quantity,
        price=new_order_item.price
        )
        
        return order_item_response



    # READ
    def get_by_id(self, unique_item_id: int) -> OrderItemResponse:
        stmt = select(Order_Item).where(Order_Item.unique_item_id == unique_item_id)
        result = self.session.execute(stmt).scalars().first()
        
        order_item_response = OrderItemResponse(
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
        
