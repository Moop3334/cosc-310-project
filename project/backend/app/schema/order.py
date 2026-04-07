import datetime
from typing import List
from pydantic import BaseModel, Field, NonNegativeInt, PositiveFloat
from app.schema.shopping_cart import CartItem

class Order(BaseModel):
    id: NonNegativeInt
    user_id: NonNegativeInt
    restaurant_id: NonNegativeInt
    items: List[CartItem]
    total_price: PositiveFloat
    creation_date: datetime.datetime = Field(default_factory=datetime.datetime.now)
    status: str = Field(min_length=1)

    def calculateTotal(self):
        return (self.price * 1.05) + 3
    #TODO: Refactor later so tax and delivery fee are not hard coded, also potentially move to services file under payment.
