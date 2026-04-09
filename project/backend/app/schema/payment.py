#Can be further improved later will need access to the order.py file to import total from.
from datetime import datetime
#from order import Order
from pydantic import BaseModel

class Payment(BaseModel):
    id: int
    total: float
    card_number: int
    expiry_date: str
    cvv: int

    def validateCard(self):
        card_str = str(self.card_number)
        if len(card_str) == 16 and len(str(self.cvv)) in [3, 4]:
            return True
        return False

    def authorisePayment(self):
        if self.total >= 0 and self.validateCard():
            return True
        return False

class PaymentResponse(BaseModel):
    success: bool
    message: str
    transaction_id: str = None

dummy_payment_info = {
    'id': 101,
    'total': 40.99,
    'card_number': 1111222233334444,
    'expiry_date': "16/10/2024",
    'cvv': 123
}

#try:
    #User(dummy_payment_info)
#except ValidationError as e:
    #print(e.errors())
