from typing import List
import datetime
from pydantic import BaseModel, Field
from app.schema.menuItems import MenuItem

class Restaurant(BaseModel):
    id: int
    name: str
    address: str
    openTimes: List[datetime.datetime] = Field(default_factory=list)
    closeTimes: List[datetime.datetime] = Field(default_factory=list)
    menu: List[MenuItem] = Field(default_factory=list)
    #openDays has been removed in favour of consolidating it into openTimes/closeTimes
    #menu has been added to keep track of which menu items belong to each restaurant

class RestaurantCreate(BaseModel):
    name: str
    address: str
    openTimes: List[datetime.datetime] = Field(default_factory=list)
    closeTimes: List[datetime.datetime] = Field(default_factory=list)
    menu: List[MenuItem] = Field(default_factory=list)

class RestaurantUpdate(BaseModel):
    name: str
    address: str
    openTimes: List[datetime.datetime] = Field(default_factory=list)
    closeTimes: List[datetime.datetime] = Field(default_factory=list)
    menu: List[MenuItem] = Field(default_factory=list)
