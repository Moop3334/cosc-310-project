# defines API endpoints/urls, groups related endpoints/scripts together and keeps main.py clean
from typing import List
from fastapi import APIRouter
from app.schema.resturant import Restaurant, RestaurantCreate, RestaurantUpdate
from app.services.restaurant_service import list_restaurants, create_restaurant, update_restaurant, delete_restaurant, get_restaurant_by_id

router = APIRouter(prefix="/restaurants", tags=["restaurants"])

@router.get("", response_model=List[Restaurant])
def get_restaurants():
    return list_restaurants()

@router.post("", response_model=Restaurant, status_code=201)
def post_restaurant(payload: RestaurantCreate):
    return create_restaurant(payload)

@router.get("/{restaurant_id}", response_model=Restaurant, status_code=201)
def get_r_by_id(restaurant_id: int):
    return get_restaurant_by_id(restaurant_id=restaurant_id)

@router.post("/{restaurant_id}", response_model=Restaurant, status_code=201)
def post_restaurant_update(restaurant_id: int,payload: RestaurantUpdate):
    return update_restaurant(restaurant_id, payload)

@router.delete("/{restaurant_id}", response_model=None, status_code=201)
def delete_r(restaurant_id: int):
    return delete_restaurant(restaurant_id)