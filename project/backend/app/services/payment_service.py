from fastapi import HTTPException
from app.schema.payment import Payment
from app.services.order_service import get_specific_order

def calculate_subtotal(order_id: int) -> float:
    order = get_specific_order(order_id)
    cart = order.items
    return sum(item.price * item.quantity for item in cart)

def calculate_total(order_id: int) -> float:
    return (calculate_subtotal(order_id) * 1.05) + 3 #Magic numbers, please change to literals to make it easier to understand