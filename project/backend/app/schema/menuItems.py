from pydantic import BaseModel, Field, NonNegativeInt, PositiveFloat

class MenuItem(BaseModel):
    id: int = NonNegativeInt
    restaurant_id: int = NonNegativeInt
    item_name: str = Field(min_length=1)
    price: float = PositiveFloat
    description: str = Field(min_length=1)
    image: str = Field(min_length=1)
    #The image attribute will be the path/url of the desired image, might not be necessary

class MenuItemCreate(BaseModel):
    item_name: str = Field(min_length=1)
    restaurant_id: int = NonNegativeInt
    price: float = PositiveFloat
    description: str = Field(min_length=1)
    image: str = Field(min_length=1)

class MenuItemUpdate(BaseModel):
    item_name: str = Field(min_length=1)
    restaurant_id: int = NonNegativeInt
    price: float = PositiveFloat
    description: str = Field(min_length=1)
    image: str = Field(min_length=1)
