from typing import List
from fastapi import HTTPException
from app.schema.payment import Payment
from app.schema.shopping_cart import CartItem

def calculate_subtotal(cart: List[CartItem]) -> float:
    return sum(item.price * item.quantity for item in cart)

def calculate_total(cart: List[CartItem]) -> float:
    return (calculate_subtotal(cart) * 1.05) + 3 #Magic numbers, please change to literals to make it easier to understand