import datetime
from typing import List
from fastapi import HTTPException
from app.schema.review import Review, ReviewCreate
from app.repositories.review_repos import (
    load_all_reviews,
    load_reviews_by_user,
    load_reviews_by_restaurant,
    load_reviews_by_item,
    save_all_reviews,
)


def dict_to_review(review_dict) -> Review:
    return Review(
        id=int(review_dict.get("id", 0)),
        user_id=int(review_dict.get("user_id", 0)),
        restaurant_id=int(review_dict.get("restaurant_id", 0)),
        order_id=int(review_dict.get("order_id", 0)),
        item_id=int(review_dict.get("item_id", 0)),
        item_name=review_dict.get("item_name", ""),
        rating=int(review_dict.get("rating", 1)),
        comment=review_dict.get("comment", ""),
        created_at=review_dict.get("created_at", datetime.datetime.now()),
    )


def list_all_reviews() -> List[Review]:
    return [dict_to_review(r) for r in load_all_reviews()]


def get_reviews_for_user(user_id: int) -> List[Review]:
    return [dict_to_review(r) for r in load_reviews_by_user(user_id)]


def get_reviews_for_restaurant(restaurant_id: int) -> List[Review]:
    return [dict_to_review(r) for r in load_reviews_by_restaurant(restaurant_id)]


def get_reviews_for_item(restaurant_id: int, item_id: int) -> List[Review]:
    return [dict_to_review(r) for r in load_reviews_by_item(restaurant_id, item_id)]


def create_review(user_id: int, payload: ReviewCreate) -> Review:
    reviews = load_all_reviews()

    # Prevent duplicate review for same user + order + item
    for r in reviews:
        if (
            int(r["user_id"]) == user_id
            and int(r["order_id"]) == payload.order_id
            and int(r["item_id"]) == payload.item_id
        ):
            raise HTTPException(
                status_code=400,
                detail="You have already reviewed this item for this order.",
            )

    new_id = len(reviews) + 1
    new_review = Review(
        id=new_id,
        user_id=user_id,
        restaurant_id=payload.restaurant_id,
        order_id=payload.order_id,
        item_id=payload.item_id,
        item_name=payload.item_name,
        rating=payload.rating,
        comment=payload.comment or "",
        created_at=datetime.datetime.now(),
    )
    reviews.append(new_review.model_dump())
    save_all_reviews(reviews)
    return new_review


def delete_review(review_id: int, user_id: int) -> str:
    reviews = load_all_reviews()
    for idx, r in enumerate(reviews):
        if int(r["id"]) == review_id:
            if int(r["user_id"]) != user_id:
                raise HTTPException(status_code=403, detail="You can only delete your own reviews.")
            del reviews[idx]
            save_all_reviews(reviews)
            return f"Review {review_id} deleted successfully."
    raise HTTPException(status_code=404, detail=f"Review {review_id} not found.")
