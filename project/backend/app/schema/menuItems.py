from pydantic import BaseModel

class MenuItem(BaseModel):
    id: int
    name: str
    price: float
    description: str
    image: str
    #The image attribute will be the path/url of the desired image

class MenuItemCreate(BaseModel):
    name: str
    price: float
    description: str
    image: str

class MenuItemUpdate(BaseModel):
    name: str
    price: float
    description: str
    image: str
