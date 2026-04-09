from typing import List
from fastapi import APIRouter, HTTPException
from app.schema.review import Review, ReviewCreate
from app.services.review_service import (
    list_all_reviews,
    get_reviews_for_user,
    get_reviews_for_restaurant,
    get_reviews_for_item,
    create_review,
    delete_review,
)

router = APIRouter(prefix="/reviews", tags=["reviews"])


@router.get("", response_model=List[Review])
def get_all_reviews():
    return list_all_reviews()


@router.get("/user/{user_id}", response_model=List[Review])
def get_user_reviews(user_id: int):
    return get_reviews_for_user(user_id)


@router.get("/restaurant/{restaurant_id}", response_model=List[Review])
def get_restaurant_reviews(restaurant_id: int):
    return get_reviews_for_restaurant(restaurant_id)


@router.get("/restaurant/{restaurant_id}/item/{item_id}", response_model=List[Review])
def get_item_reviews(restaurant_id: int, item_id: int):
    return get_reviews_for_item(restaurant_id, item_id)


@router.post("/{user_id}", response_model=Review, status_code=201)
def post_review(user_id: int, payload: ReviewCreate):
    return create_review(user_id, payload)


@router.delete("/{review_id}", response_model=str)
def remove_review(review_id: int, user_id: int):
    return delete_review(review_id, user_id)
