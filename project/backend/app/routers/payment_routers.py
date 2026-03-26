from fastapi import APIRouter, HTTPException
from app.schema.payment import Payment
from app.services.payment_service import calculate_total

router = APIRouter(prefix="/payments", tags=["payments"])

@router.get("/{order_id}/total", response_model=float)
def get_total(order_id: str):
    return calculate_total(order_id)