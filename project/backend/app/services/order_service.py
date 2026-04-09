from typing import List, Optional
import datetime
from fastapi import HTTPException
from app.schema.order import Order
from app.schema.shopping_cart import CartItem
from app.repositories.order_repos import load_all_order, load_specific_order, save_all_orders
from app.repositories.delivery_repos import save_a_delivery
from app.services.cart_service import clear_cart, get_cart
from app.services.payment_service import calculate_subtotal, calculate_total

def dict_to_order(order_dict) -> Order:
    """Convert a dictionary from CSV to an Order object."""
    items = []
    if order_dict.get("items"):
        for item_data in order_dict["items"]:
            items.append(CartItem(
                item_id=int(item_data.get("item_id", 0)),
                item_name=item_data.get("item_name", ""),
                quantity=int(item_data.get("quantity", 1)),
                price=float(item_data.get("price", 0.0))
            ))
    
    return Order(
        id=int(order_dict.get("id", 0)),
        user_id=int(order_dict.get("user_id", 0)),
        restaurant_id=int(order_dict.get("restaurant_id", 0)),
        items=items,
        total_price=calculate_subtotal(items),
        creation_date=order_dict.get("creation_date"),
        status=order_dict.get("status", "Pending Approval")
    )

def list_orders(restaurant_id: Optional[int] = None) -> List[Order]:
    o_list = []
    for o in load_all_order():
        o_list.append(dict_to_order(o))
    if restaurant_id is not None:
        o_list = [order for order in o_list if order.restaurant_id == restaurant_id]
    return o_list

def get_specific_order(order_id: int) -> Order:
    o = load_specific_order(order_id)
    return dict_to_order(o)

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
        total_price=calculate_total(cart.items), #TODO: need to refactor payment method to accept list of items
        creation_date=datetime.datetime.now(),
        status="Pending Approval"
    )
    
    orders.append(new_order)
    save_all_orders(orders)
    clear_cart(user_id)

    return new_order

def update_order_status(order_id: int, new_status: str) -> str:
    orders = load_all_order()
    for idx, order in enumerate(orders):
        if int(order["id"]) == order_id:
            orders[idx]["status"] = new_status
            save_all_orders(orders)
            return f"Status with order id {order_id} updated successfully."
    raise IndexError(f"Error: Unable to find order id:{order_id}")

def delete_specific_order(order_id: int) -> str:
    orders = load_all_order()
    for idx, order in enumerate(orders):
        if int(order["id"]) == order_id:
            del orders[idx]
            save_all_orders(orders)
            return f"Order with id {order_id} deleted successfully."
    raise IndexError(f"Error: Unable to find order id:{order_id}")

def complete_an_order(order_id: int) -> str:
    orders = load_all_order()
    for idx, order in enumerate(orders):
        if int(order.get("id", 0)) == order_id:
            orders[idx]["status"] = "Completed"
            
            # Convert items list to comma-separated string
            items_str = ", ".join([f"{item.get('item_name', '')} (qty: {item.get('quantity', 1)})" for item in order.get("items", [])])
            
            save_a_delivery({
               "order_id": order_id,
               "restaurant_id": order["restaurant_id"],
               "food_item": items_str,
               "order_time": order["creation_date"],
               "delivery_time": None,
               "delivery_distance": None,
               "order_value": order["total_price"],
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
            save_all_orders(orders)
            return f"Order with id {order_id} completed successfully."
    raise IndexError(f"Error: Unable to find order id:{order_id}")