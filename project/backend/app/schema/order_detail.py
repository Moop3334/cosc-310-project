from app.schema.menu_items import MenuItem
from pydantic import BaseModel

class OrderItem(BaseModel):
    item: str
    quantity: int

    def calculateSubTotal(self):
        return self.item.price * self.quantity
