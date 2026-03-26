from fastapi import HTTPException
from app.schema.payment import payment
from app.services.order_service import get_specific_order

def calculate_total(order_id: int) -> float:
    order = get_specific_order(order_id)
    return (order.price * 1.05) + 3