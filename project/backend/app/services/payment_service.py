from typing import List
from fastapi import HTTPException
from app.schema.payment import Payment
from app.schema.shopping_cart import CartItem
from app.services.order_service import get_specific_order

def calculate_subtotal(cart: List[CartItem]) -> float:
    return sum(item.price * item.quantity for item in cart)

def calculate_total(order_id: int) -> float:
    order = get_specific_order(order_id)
    return (calculate_subtotal(order.items) * 1.05) + 3 #Magic numbers, please change to literals to make it easier to understand