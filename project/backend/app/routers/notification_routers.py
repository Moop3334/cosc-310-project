from typing import List
from fastapi import APIRouter
from app.schema.notification import Notification
from app.services.notification_service import get_user_notifications, mark_as_read

router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.get("/{user_id}", response_model=List[Notification])
def get_notifications(user_id: int):
    return get_user_notifications(user_id)


@router.patch("/{user_id}/read", response_model=str)
def read_notifications(user_id: int):
    return mark_as_read(user_id)