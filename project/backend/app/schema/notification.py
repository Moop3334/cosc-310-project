from typing import List
from datetime import datetime
from pydantic import BaseModel, Field, NonNegativeInt

class NotificationItem(BaseModel):
    item_id: NonNegativeInt
    item_name: str = Field(min_length=1)
    time: datetime.utcnow = Field(ge=1)

class Notification(BaseModel):
    user_id: NonNegativeInt
    Notifications: List[NotificationItem] = Field(default_factory=list)