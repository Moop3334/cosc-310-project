from typing import List
import datetime
from enum import Enum
from pydantic import BaseModel, Field
from app.schema.orderDetail import OrderItem


class Order(BaseModel):
    id: int
    user_id: int
    restaurant_id: int
    item: str
    price: float
    creation_date: datetime.datetime
    status: str

    def calculateTotal(self):
        return sum(item.calculateSubTotal() for item in self.items) * 1.05
    #Tax calculation can be improved and delivery fee can be added in future
