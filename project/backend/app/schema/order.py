from orderDetail import OrderItem
from customer import Customer
from resturant import Restaurant
from typing import List
import datetime
from pydantic import BaseModel, Field

class OrderStatus(str, Enum):
    PENDING = "pending approval"
    PREPARING = "preparing order"
    DELIVERING = "out for delivery"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
#Can be used to create update status methods in other classes
#Should hopefully help to keep status messages consistent when updating across classes

class Order(BaseModel):
    id: int
    customer: Customer
    restaurant: Restaurant
    items: List[OrderItem] = Field(default_factory=list)
    creation_date: datetime = datetime.now()
    status: OrderStatus = OrderStatus.PENDING
    

    def calculateTotal(self):
        return sum(item.calculateSubTotal() for item in self.items) * 1.05
    #Tax calculation can be improved and delivery fee can be added in future

