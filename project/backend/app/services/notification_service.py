import datetime
from typing import List
from app.schema.notification import Notification
from app.repositories.notification_repos import (
    load_all_notifications,
    load_notifications_by_user,
    save_all_notifications,
)


def dict_to_notification(n_dict) -> Notification:
    return Notification(
        id=int(n_dict.get("id", 0)),
        user_id=int(n_dict.get("user_id", 0)),
        order_id=int(n_dict.get("order_id", 0)),
        message=n_dict.get("message", ""),
        is_read=str(n_dict.get("is_read", "False")).lower() == "true",
        created_at=n_dict.get("created_at", datetime.datetime.now()),
    )


def get_user_notifications(user_id: int) -> List[Notification]:
    rows = load_notifications_by_user(user_id)
    return [dict_to_notification(r) for r in rows]


def create_notification(user_id: int, order_id: int, message: str) -> Notification:
    all_notifications = load_all_notifications()
    new_id = len(all_notifications) + 1
    new_notification = Notification(
        id=new_id,
        user_id=user_id,
        order_id=order_id,
        message=message,
        is_read=False,
        created_at=datetime.datetime.now(),
    )
    all_notifications.append(new_notification.model_dump())
    save_all_notifications(all_notifications)
    return new_notification


def mark_as_read(user_id: int) -> str:
    all_notifications = load_all_notifications()
    updated = 0
    for n in all_notifications:
        if int(n["user_id"]) == user_id and str(n["is_read"]).lower() != "true":
            n["is_read"] = "True"
            updated += 1
    save_all_notifications(all_notifications)
    return f"Marked {updated} notifications as read."
