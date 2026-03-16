from app.schema.menuItems import MenuItem
from pydantic import BaseModel

class OrderItem(BaseModel):
    item: MenuItem
    quantity: int

    def calculateSubTotal(self):
        return self.item.price * self.quantity
