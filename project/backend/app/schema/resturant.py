from pydantic import BaseModel
from typing import List
import datetime

class Resturant(BaseModel):
    id: int
    name: str
    address: str
    openTimes = List[datetime.datetime] = []
    closeTimes = List[datetime.datetime] = []
    #openDays has been removed in favour of consolidating it into openTimes/closeTimes using the datetime class

class ItemCreate(BaseModel):
    title: str
    category: str
    tags: List[str] = []

class ItemUpdate(BaseModel):
    title : str
    category:str
    tags: List[str] = []