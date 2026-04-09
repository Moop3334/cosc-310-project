import datetime
from pydantic import BaseModel, Field, NonNegativeInt


class Notification(BaseModel):
    id: NonNegativeInt
    user_id: NonNegativeInt
    order_id: NonNegativeInt
    message: str = Field(min_length=1)
    is_read: bool = False
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)