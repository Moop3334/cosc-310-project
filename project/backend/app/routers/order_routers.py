from typing import List
from fastapi import APIRouter, HTTPException
from app.schema.order import Order
from app.services.order_service import list_orders, get_specific_order, delete_specific_order, save_an_order, update_order_status

router = APIRouter(prefix="/orders", tags=["orders"])

@router.get("", response_model=List[Order])
def get_orders():
    return list_orders()

@router.get("/{order_id}", response_model=Order)
def get_order(order_id: str):
    return get_specific_order(order_id)

@router.post("/{order_id}", response_model=str)
def create_order(new_uid: int, new_rid: int, new_item: str):
    return save_an_order(new_uid, new_rid, new_item)

@router.delete("/{order_id}", response_model=str)
def delete_order(order_id: str):
    return delete_specific_order(order_id)

@router.post("/{order_id}/status", response_model=str)
def update_status(order_id: str, new_status: str):
    return update_order_status(order_id, new_status)