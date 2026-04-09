from pathlib import Path
import csv
from typing import Dict, Any, List

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "reviews.csv"

FIELD_NAMES = ["id", "user_id", "restaurant_id", "order_id", "item_id", "item_name", "rating", "comment", "created_at"]


def load_all_reviews() -> List[Dict[str, Any]]:
    if not DATA_PATH.exists():
        raise FileExistsError(
            "Error: The storage csv does not exist or otherwise cannot be accessed"
        )
    reviews = []
    with DATA_PATH.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f, delimiter=",")
        for row in reader:
            reviews.append(row)
    return reviews


def load_reviews_by_user(user_id: int) -> List[Dict[str, Any]]:
    reviews = load_all_reviews()
    return [r for r in reviews if int(r["user_id"]) == user_id]


def load_reviews_by_restaurant(restaurant_id: int) -> List[Dict[str, Any]]:
    reviews = load_all_reviews()
    return [r for r in reviews if int(r["restaurant_id"]) == restaurant_id]


def load_reviews_by_item(restaurant_id: int, item_id: int) -> List[Dict[str, Any]]:
    reviews = load_all_reviews()
    return [
        r for r in reviews
        if int(r["restaurant_id"]) == restaurant_id and int(r["item_id"]) == item_id
    ]


def save_all_reviews(reviews: List[Dict[str, Any]]) -> None:
    with DATA_PATH.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELD_NAMES)
        writer.writeheader()
        for review in reviews:
            row = {
                "id": str(review.get("id", "")),
                "user_id": str(review.get("user_id", "")),
                "restaurant_id": str(review.get("restaurant_id", "")),
                "order_id": str(review.get("order_id", "")),
                "item_id": str(review.get("item_id", "")),
                "item_name": str(review.get("item_name", "")),
                "rating": str(review.get("rating", "")),
                "comment": str(review.get("comment", "")),
                "created_at": str(review.get("created_at", "")),
            }
            writer.writerow(row)
