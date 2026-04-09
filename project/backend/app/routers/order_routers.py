from typing import List, Optional
from fastapi import APIRouter, HTTPException
from app.schema.order import Order
from app.services.order_service import list_orders, get_specific_order, delete_specific_order, update_order_status, complete_an_order, checkout
from pydantic import BaseModel

#TODO: update to use shopping cart instead of menu item

router = APIRouter(prefix="/orders", tags=["orders"])


class StatusUpdate(BaseModel):
    status: str

@router.get("", response_model=List[Order])
def get_orders(restaurant_id: Optional[int] = None):
    return list_orders(restaurant_id)

@router.get("/{order_id}", response_model=Order)
def get_order(order_id: int):
    """Get a specific order by ID."""
    try:
        return get_specific_order(order_id)
    except IndexError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/{user_id}/checkout", response_model=Order)
def checkout_order(user_id: int):
    """Create an order from the user's shopping cart."""
    try:
        order = checkout(user_id)
        return order
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/{order_id}/status", response_model=str)
def update_status(order_id: int, payload: StatusUpdate):
    """Update the status of an order."""
    try:
        return update_order_status(order_id, payload.status)
    except IndexError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{order_id}", response_model=str)
def delete_order(order_id: int):
    """Delete an order."""
    try:
        return delete_specific_order(order_id)
    except IndexError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/{order_id}/complete", response_model=str)
def complete_order(order_id: int):
    """Mark an order as completed and create a delivery record."""
    try:
        return complete_an_order(order_id)
    except IndexError as e:
        raise HTTPException(status_code=404, detail=str(e))