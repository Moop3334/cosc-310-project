from menuItems import MenuItem
from restaurant import Restaurant
from customer import Customer
from typing import List
import datetime
from pydantic import BaseModel, Field

class Order(BaseModel):
    id: int
    customer: Customer
    items: List[OrderItem] = Field(default_factory=list)
    creation_date: datetime = datetime.now()
    status: str = "pending approval"
    #Will add method to update status later

    def calculateTotal(self):
        return sum(item.calculateSubTotal() for item in self.items) * 1.05
    #Tax calculation can be improved and delivery fee can be added in future

