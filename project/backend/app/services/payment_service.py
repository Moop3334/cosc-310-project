from typing import List
from fastapi import HTTPException
from app.schema.payment import Payment
from app.schema.shopping_cart import CartItem

gst = 1.05
delivery_fee = 3
def calculate_subtotal(items: List[CartItem]) -> float:
    return sum(item.price * item.quantity for item in items)

def calculate_total(items: List[CartItem]) -> float:
    return (calculate_subtotal(items) * gst) + delivery_fee