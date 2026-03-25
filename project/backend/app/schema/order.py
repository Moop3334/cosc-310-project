from typing import List
import datetime
from enum import Enum
from pydantic import BaseModel, Field
from app.schema.orderDetail import OrderItem

class OrderStatus(str, Enum):
    PENDING = "Pending Approval"
    PREPARING = "Preparing Order"
    DELIVERING = "Out for Delivery"
    DELIVERED = "Delivered"
    CANCELLED = "Cancelled"
#Can be used to create update status methods in other classes
#Should hopefully help to keep status messages consistent when updating across classes

class Order(BaseModel):
    id: str
    user_id: str
    restaurant_id: str
    items: str
    creation_date: datetime.datetime
    status: str

    def calculateTotal(self):
        return sum(item.calculateSubTotal() for item in self.items) * 1.05
    #Tax calculation can be improved and delivery fee can be added in future
