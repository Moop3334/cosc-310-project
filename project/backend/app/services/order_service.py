from typing import List
import datetime
from fastapi import HTTPException
from app.schema.order import Order
from app.repositories.order_repos import load_all_order, load_specific_order, save_all_orders
from app.repositories.delivery_repos import save_a_delivery
from app.services.cart_service import clear_cart, get_cart

#TODO: update to use shopping cart instead of menu item

def list_orders() -> List[Order]:
    o_list = []
    for o in load_all_order():
        o_list.append(
            Order(
                id=o.get("id"),
                user_id=o.get("user_id"),
                restaurant_id=o.get("restaurant_id"),
                item=o.get("item"),
                price=o.get("price"),
                creation_date=o.get("creation_date"),
                status=o.get("status")
            ))
    return o_list

def get_specific_order(order_id: int) -> Order:
    o = load_specific_order(order_id)
    return Order(
        id=o.get("id"),
        user_id=o.get("user_id"),
        restaurant_id=o.get("restaurant_id"),
        item=o.get("item"),
        price=o.get("price"),
        creation_date=o.get("creation_date"),
        status=o.get("status")
    )

def checkout(user_id: int) -> Order:
    cart = get_cart(user_id)
    if not cart or not cart.items:
        raise ValueError("Error: Cart is empty")
    
    orders = list_orders()
    new_id = len(orders) + 1

    new_order = Order(
        id=new_id,
        user_id=user_id,
        restaurant_id=cart.restaurant_id,
        items=cart.items,
        price=cart.total * 1.05 + 3, #TODO: need to refactor payment method to accept list of items
        creation_date=datetime.datetime.now(),
        status="Pending Approval"
    )

    orders.append(new_order.model_dump())
    save_all_orders(orders)
    clear_cart(user_id)

    return new_order

#NOTE: Only here until all references can be changed to use the checkout method instead
def save_an_order(new_uid: int, new_rid: int, new_item: str, new_price: float) -> str:
    orders = list_orders()
    new_id = len(orders) + 1
    new_order = Order(
        id=new_id,
        user_id=new_uid,
        restaurant_id=new_rid,
        item=new_item,
        price=new_price,
        creation_date=datetime.datetime.now(),
        status="Pending Approval"
    )
    orders.append(new_order.dict())
    save_all_orders(orders)
    return f"Order with id {new_id} created successfully."

def update_order_status(order_id: int, new_status: str) -> str:
    orders = load_all_order()
    for idx, order in enumerate(orders):
        if order["id"] == order_id:
            orders[idx]["status"] = new_status
            save_all_orders(orders)
            return f"Status with order id {order_id} updated successfully."
    raise IndexError(f"Error: Unable to find order id:{order_id}")

def delete_specific_order(order_id: int) -> str:
    orders = load_all_order()
    for idx, order in enumerate(orders):
        if order["id"] == order_id:
            del orders[idx]
            save_all_orders(orders)
            return f"Order with id {order_id} deleted successfully."
    raise IndexError(f"Error: Unable to find order id:{order_id}")

def complete_an_order(order_id: int) -> str:
    orders = load_all_order()
    for idx, order in enumerate(orders):
        if order["id"] == order_id:
            orders[idx]["status"] = "Completed"
            save_a_delivery({
               "order_id": order_id,
               "restaurant_id": order["restaurant_id"],
               "food_item": order["item"],
               "order_time": order["creation_date"],
               "delivery_time": None,
               "delivery_distance": None,
               "order_value": order["price"],
               "delivery_method": None,
               "traffic_condition": None,
               "weather_condition": None,
               "delivery_time_actual": None,
               "delivery_delay": None,
               "route_taken": None,
               "customer_id": order["user_id"],
               "age": None,
               "gender": None,
               "location": None,
               "order_history": None,
               "customer_rating": None,
               "preferred_cuisine": None,
               "order_frequency": None,
               "loyalty_program": None,
               "food_temperature": None,
               "food_freshness": None,
               "packaging_quality": None,
               "food_condition": None,
               'customer_satisfaction': None, 
                'small_route': None, 
                'bike_friendly_route': None, 
                'route_type': None, 
                'route_efficiency': None, 
                'predicted_delivery_mode': None, 
                'traffic_avoidance': None
            })
            delete_specific_order(order_id)
            return f"Order with id {order_id} completed successfully."
    raise IndexError(f"Error: Unable to find order id:{order_id}")