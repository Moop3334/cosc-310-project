from typing import List
import datetime
from enum import Enum
from orderDetail import OrderItem
from user import User
from resturant import Restaurant
#need pull request accepted to get user & restaurant files
from pydantic import BaseModel, Field

class OrderStatus(str, Enum):
    PENDING = "Pending Approval"
    PREPARING = "Preparing Order"
    DELIVERING = "Out for Delivery"
    DELIVERED = "Delivered"
    CANCELLED = "Cancelled"
#Can be used to create update status methods in other classes
#Should hopefully help to keep status messages consistent when updating across classes

class Order(BaseModel):
    id: int
    user: User
    restaurant: Restaurant
    items: List[OrderItem] = Field(default_factory=list)
    creation_date: datetime
    status: OrderStatus = OrderStatus.PENDING

    def calculateTotal(self):
        return sum(item.calculateSubTotal() for item in self.items) * 1.05
    #Tax calculation can be improved and delivery fee can be added in future
