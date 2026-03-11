# defines API endpoints/urls, groups related endpoints/scripts together and keeps main.py clean
from typing import List
from fastapi import APIRouter, status
from schema.resturant import Restaurant, RestaurantCreate, RestaurantUpdate
#from services.items_service import list_items, create_item, delete_item, update_item

router = APIRouter(prefix="/items", tags=["items"])

@router.get("", response_model=List[Restaurant])
def get_items():
    return ""

#simple post the payload (is the body of the request)
"""
@router.post("", response_model=Restaurant, status_code=201)
def post_item(payload: RestaurantCreate):
    return create_item(payload)
"""