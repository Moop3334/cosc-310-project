from typing import List
from fastapi import APIRouter, HTTPException
from app.schema.order import Order
from app.services.order_service import list_orders, get_specific_order, delete_specific_order, save_an_order, update_order_status, complete_an_order, checkout

#TODO: update to use shopping cart instead of menu item

router = APIRouter(prefix="/orders", tags=["orders"])

@router.get("", response_model=List[Order])
def get_orders():
    return list_orders()

@router.get("/{order_id}", response_model=Order)
def get_order(order_id: str):
    return get_specific_order(order_id)

@router.post("/{user_id}/checkout")
def checkout(user_id: int):
    try:
        order = checkout(user_id)
        return order
    except ValueError:
        raise HTTPException(status_code=404, detail="Error: cart doesn't exist or is empty.")

#TODO: remove when save_an_order is removed
@router.post("", response_model=str)
def create_order(new_uid: int, new_rid: int, new_item: str, new_price: float):
    return save_an_order(new_uid, new_rid, new_item, new_price)

@router.post("/{order_id}/status", response_model=str)
def update_status(order_id: str, new_status: str):
    return update_order_status(order_id, new_status)

@router.delete("/{order_id}", response_model=str)
def delete_order(order_id: str):
    return delete_specific_order(order_id)

@router.post("/{order_id}/complete", response_model=str)
def complete_order(order_id: str):
    return complete_an_order(order_id)