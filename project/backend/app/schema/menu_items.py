from pydantic import BaseModel, Field, NonNegativeInt, PositiveFloat

class MenuItem(BaseModel):
    id: NonNegativeInt
    restaurant_id: NonNegativeInt
    item_name: str = Field(min_length=1)
    price: PositiveFloat
    description: str = Field(min_length=1)

class MenuItemCreate(BaseModel):
    item_name: str = Field(min_length=1)
    restaurant_id: NonNegativeInt
    price: PositiveFloat
    description: str = Field(min_length=1)

class MenuItemUpdate(BaseModel):
    item_name: str = Field(min_length=1)
    restaurant_id: NonNegativeInt 
    price: PositiveFloat
    description: str = Field(min_length=1)
