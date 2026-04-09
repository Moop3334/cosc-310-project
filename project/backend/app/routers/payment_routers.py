from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.schema.payment import Payment, PaymentResponse
from app.services.payment_service import calculate_total, process_payment
from app.services.order_service import get_specific_order

router = APIRouter(prefix="/payments", tags=["payments"])

class PaymentRequest(BaseModel):
    cardNumber: str
    expiryDate: str
    cvv: str
    cardholderName: str
    total: float

@router.post("/process", response_model=PaymentResponse)
def process_payment_endpoint(payment_data: PaymentRequest):
    """Process a payment for an order."""
    try:
        # Create payment object
        payment = Payment(
            id=0,  # Will be set by service
            total=payment_data.total,
            card_number=int(payment_data.cardNumber),
            expiry_date=payment_data.expiryDate,
            cvv=int(payment_data.cvv)
        )

        # Process the payment
        result = process_payment(payment)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Payment processing failed: {str(e)}")

@router.get("/{order_id}/total", response_model=float)
def get_total(order_id: str):
    return calculate_total(get_specific_order(order_id).items)