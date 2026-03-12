#Can be further improved later will need access to the order.py file to import total from.
import datetime
#from order import Order
from pydantic import BaseModel

class Payment(BaseModel):
    id: int
    total: float
    card_number: int
    expiry_date: datetime
    cvv: int
    #Should import from user class in future

    def validateCard(self):
        if(self.cardNumber.length==16 and self.expiryDate.length==4 and self.cvv.length==3):
            return True

        return False

    def authorisePayment(self):
        if self.total >= 0:
            return True

        return False

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
