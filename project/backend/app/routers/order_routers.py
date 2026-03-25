from typing import List
from fastapi import APIRouter
from app.schema.order import Order
from app.services.order_service import list_orders, get_specific_order

router = APIRouter(prefix="/orders", tags=["orders"])

@router.get("", response_model=List[Order])
def get_orders():
    return list_orders()

@router.get("/{order_id}", response_model=Order)
def get_order(order_id: str):
    return get_specific_order(order_id)
