import datetime
from typing import Optional
from pydantic import BaseModel, Field, NonNegativeInt


class Review(BaseModel):
    id: NonNegativeInt
    user_id: NonNegativeInt
    restaurant_id: NonNegativeInt
    order_id: NonNegativeInt
    item_id: NonNegativeInt
    item_name: str = Field(min_length=1)
    rating: int = Field(ge=1, le=5)
    comment: str = ""
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)


class ReviewCreate(BaseModel):
    restaurant_id: NonNegativeInt
    order_id: NonNegativeInt
    item_id: NonNegativeInt
    item_name: str = Field(min_length=1)
    rating: int = Field(ge=1, le=5)
    comment: Optional[str] = ""
