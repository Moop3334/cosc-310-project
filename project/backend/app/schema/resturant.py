from pydantic import BaseModel
from typing import List
from menuItems import MenuItem
import datetime

class Resturant(BaseModel):
    id: int
    name: str
    address: str
    openTimes = List[datetime.datetime] = []
    closeTimes = List[datetime.datetime] = []
    menu = List[MenuItem] = []
    #openDays has been removed in favour of consolidating it into openTimes/closeTimes using the datetime class
    #menu has been added to keep track of which menu items belong to each restaurant

class RestaurantCreate(BaseModel):
    name: str
    address: str
    openTimes = List[datetime.datetime] = []
    closeTimes = List[datetime.datetime] = []
    menu = List[MenuItem] = []

class RestaurantUpdate(BaseModel):
    name: str
    address: str
    openTimes = List[datetime.datetime] = []
    closeTimes = List[datetime.datetime] = []
    menu = List[MenuItem] = []