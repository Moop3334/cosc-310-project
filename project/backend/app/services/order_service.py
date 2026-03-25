from typing import List
import datetime
from fastapi import HTTPException
from app.schema.order import Order
from app.repositories.order_repos import load_all_order, load_specific_order

def list_orders() -> List[Order]:
    
    o_list = []
    for o in load_all_order():
        o_list.append(
            Order(
                id=o.get("id"),
                user_id=o.get("user_id"),
                restaurant_id=o.get("restaurant_id"),
                items=o.get("item"),
                creation_date=o.get("creation_date"),
                status=o.get("status")
            ))
    return o_list

def get_specific_order(order_id: str) -> Order:
    o = load_specific_order(order_id)
    return Order(
        id=o.get("id"),
        user_id=o.get("user_id"),
        restaurant_id=o.get("restaurant_id"),
        items=o.get("item"),
        creation_date=o.get("creation_date"),
        status=o.get("status")
    )