#from menuItems import MenuItem
#need pull request accepted to get menuItem file
from pydantic import BaseModel

class OrderItem(BaseModel):
    item: str
    quantity: int

    def calculateSubTotal(self):
        return self.item.price * self.quantity