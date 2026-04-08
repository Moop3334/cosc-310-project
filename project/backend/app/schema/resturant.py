from typing import List
import datetime
from pydantic import BaseModel, Field, NonNegativeInt
from app.schema.menu_items import MenuItem,MenuItemCreate,MenuItemUpdate

class Restaurant(BaseModel):
    id: NonNegativeInt = Field(ge=0)
    name: str = Field(min_length=1)
    address: str = Field(min_length=1)
    open_times: List[datetime.time] = Field(default_factory=list, min_length=7, max_length=7)
    close_times: List[datetime.time] = Field(default_factory=list, min_length=7, max_length=7)
    menu: List[MenuItem] = Field(default_factory=list)
    #openDays has been removed in favour of consolidating it into openTimes/closeTimes
    #menu has been added to keep track of which menu items belong to each restaurant

class RestaurantCreate(BaseModel):
    name: str = Field(min_length=1)
    address: str = Field(min_length=1)
    open_times: List[datetime.time] = Field(default_factory=list, min_length=7, max_length=7)
    close_times: List[datetime.time] = Field(default_factory=list, min_length=7, max_length=7)
    menu: List[MenuItemCreate] = Field(default_factory=list)

class RestaurantUpdate(BaseModel):
    name: str = Field(min_length=1)
    address: str = Field(min_length=1)
    open_times: List[datetime.time] = Field(default_factory=list, min_length=7, max_length=7)
    close_times: List[datetime.time] = Field(default_factory=list, min_length=7, max_length=7)
    menu: List[MenuItemUpdate] = Field(default_factory=list)
