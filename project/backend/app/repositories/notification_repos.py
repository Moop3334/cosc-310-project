from pathlib import Path
import csv
from typing import Dict, Any, List

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "notifications.csv"

FIELD_NAMES = ["id", "user_id", "order_id", "message", "is_read", "created_at"]


def load_all_notifications() -> List[Dict[str, Any]]:
    if not DATA_PATH.exists():
        raise FileExistsError(
            "Error: The storage csv does not exist or otherwise cannot be accessed"
        )
    notifications = []
    with DATA_PATH.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f, delimiter=",")
        for row in reader:
            notifications.append(row)
    return notifications


def load_notifications_by_user(user_id: int) -> List[Dict[str, Any]]:
    notifications = load_all_notifications()
    return [n for n in notifications if int(n["user_id"]) == user_id]


def save_all_notifications(notifications: List[Dict[str, Any]]) -> None:
    with DATA_PATH.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELD_NAMES)
        writer.writeheader()
        for n in notifications:
            row = {
                "id": str(n.get("id", "")),
                "user_id": str(n.get("user_id", "")),
                "order_id": str(n.get("order_id", "")),
                "message": str(n.get("message", "")),
                "is_read": str(n.get("is_read", "False")),
                "created_at": str(n.get("created_at", "")),
            }
            writer.writerow(row)

