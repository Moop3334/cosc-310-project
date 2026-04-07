from typing import List
from pydantic import BaseModel, Field, NonNegativeInt, PositiveFloat
from app.schema.menu_items import MenuItem

class ShoppingCart(BaseModel):
    user_id: NonNegativeInt
    restaurant_id: NonNegativeInt
    items: List[CartItem] = Field(default_factory=list)
    total: PositiveFloat = Field(default=0.0)

class CartItem(BaseModel):
    item_id: NonNegativeInt
    item_name: str = Field(min_length=1)
    quantity: NonNegativeInt = Field(ge=1)
    price: PositiveFloat