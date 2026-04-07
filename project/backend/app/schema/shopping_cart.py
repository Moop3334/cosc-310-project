from typing import List
from pydantic import BaseModel, Field, NonNegativeInt, PositiveFloat
from app.schema.menu_items import MenuItem

class ShoppingCart(BaseModel):
    restaurant_id: NonNegativeInt
    items: List[MenuItem]
    total: PositiveFloat