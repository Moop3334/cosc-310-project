# defines API endpoints/urls, groups related endpoints/scripts together and keeps main.py clean
from typing import List
from fastapi import APIRouter, status
from app.schema.resturant import Restaurant, RestaurantCreate, RestaurantUpdate
from app.services.restaurant_service import list_restaurants, create_restaurant, update_restaurant, delete_restaurant, get_restaurant_by_id

router = APIRouter(prefix="/items", tags=["items"])

@router.get("", response_model=List[Restaurant])
def get_items():
    return list_restaurants()

#simple post the payload (is the body of the request)

@router.post("", response_model=Restaurant, status_code=201)
def post_item(payload: RestaurantCreate):
    return create_restaurant(payload)
