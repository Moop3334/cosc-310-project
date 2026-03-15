from pydantic import BaseModel

class MenuItem(BaseModel):
    item_id: int
    item_name: str
    price: float
    description: str
    image: str
    #The image attribute will be the path/url of the desired image

class MenuItemCreate(BaseModel):
    item_name: str
    price: float
    description: str
    image: str

class MenuItemUpdate(BaseModel):
    item_name: str
    price: float
    description: str
    image: str
