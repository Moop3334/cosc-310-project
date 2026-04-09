from typing import List
from fastapi import HTTPException
from app.schema.payment import Payment, PaymentResponse
from app.schema.shopping_cart import CartItem

gst = 1.05
delivery_fee = 3
def calculate_subtotal(items: List[CartItem]) -> float:
    return sum(item.price * item.quantity for item in items)

def calculate_total(items: List[CartItem]) -> float:
    return (calculate_subtotal(items) * gst) + delivery_fee

def process_payment(payment: Payment) -> PaymentResponse:
    """Process a payment and return the result."""
    try:
        if not payment.authorisePayment():
            raise ValueError("Payment authorization failed. Please check your card details.")

        # Generate a mock transaction ID
        import uuid
        transaction_id = str(uuid.uuid4())[:8].upper()

        return PaymentResponse(
            success=True,
            message="Payment processed successfully",
            transaction_id=transaction_id
        )
    except Exception as e:
        raise ValueError(f"Payment processing failed: {str(e)}")