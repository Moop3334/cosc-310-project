# defines API endpoints/urls, groups related endpoints/scripts together and keeps main.py clean
from typing import List
from fastapi import APIRouter, HTTPException
from app.repositories.restaurant_repos import load_all_restaurants
from app.schema.resturant import Restaurant, RestaurantCreate, RestaurantUpdate
from app.schema.menu_items import MenuItem, MenuItemCreate, MenuItemUpdate
from app.services.restaurant_service import list_restaurants, create_restaurant, update_restaurant, delete_restaurant, get_restaurant_by_id, filter_restaurants
from app.services.menu_service import list_menu, get_menu_item_by_id, create_menu_item, update_menu_item, delete_menu_item, filter_menu_items

router = APIRouter(prefix="/restaurants", tags=["restaurants"])

@router.get("", response_model=List[Restaurant])
def get_restaurants(name: str | None = None):
    valid_name = ""
    if name is not None:
        valid_name = name
    if valid_name is not None and valid_name.strip() != "":
        return filter_restaurants(name)
    else:
        return list_restaurants()

@router.post("", response_model=Restaurant, status_code=201)
def post_restaurant(payload: RestaurantCreate):
    return create_restaurant(payload)

@router.get("/{restaurant_id}", response_model=Restaurant, status_code=200)
def get_restaurant(restaurant_id: int):
    return get_restaurant_by_id(restaurant_id=restaurant_id)

@router.put("/{restaurant_id}", response_model=Restaurant, status_code=200)
def put_restaurant_update(restaurant_id: int, payload: RestaurantUpdate):
    return update_restaurant(restaurant_id, payload)

@router.delete("/{restaurant_id}", response_model=None, status_code=200)
def delete_r(restaurant_id: int):
    return delete_restaurant(restaurant_id)

menu_router = APIRouter(prefix="/restaurants", tags=["menu"])  

@menu_router.get("/{restaurant_id}/menu", response_model=List[MenuItem], status_code=200)
def get_menu(restaurant_id: int, name: str | None = None):
    valid_name = ""
    if name is not None:
        valid_name = name
    if valid_name is not None and valid_name.strip() != "":
        return filter_menu_items(restaurant_id, name)
    else:
        return list_menu(restaurant_id)

@menu_router.get("/{restaurant_id}/menu/{item_id}", response_model=MenuItem, status_code=200)
def get_menu_item(restaurant_id: int, item_id: int):
    return get_menu_item_by_id(restaurant_id, item_id)

@menu_router.post("/{restaurant_id}/menu", response_model=MenuItem, status_code=201)
def post_menu_item(restaurant_id: int, payload: MenuItemCreate):
    # This check needs to be here and not in services because the create_menu_item() function is also called when creating a new restaurant, 
    # which will cause this to raise an error since the restaurant hasn't been saved yet
    restaurant_ids = [int(it["id"]) for it in load_all_restaurants()] 
    if payload.restaurant_id not in restaurant_ids:
        raise HTTPException(status_code=404, detail=f"Unable to find a restaurant with id {payload.restaurant_id}")
    return create_menu_item(restaurant_id, payload)

@menu_router.post("/{restaurant_id}/menu/{item_id}", response_model=MenuItem, status_code=201)
def post_menu_item_update(restaurant_id: int, payload: MenuItemUpdate, item_id: int):
    return update_menu_item(restaurant_id, item_id, payload)

@menu_router.put("/{restaurant_id}/menu/{item_id}", response_model=MenuItem, status_code=200)
def put_menu_item_update(restaurant_id: int, item_id: int, payload: MenuItemUpdate):
    return update_menu_item(restaurant_id, item_id, payload)

@menu_router.delete("/{restaurant_id}/menu/{item_id}", response_model=None, status_code=200)
def delete_item(restaurant_id: int, item_id: int):
    return delete_menu_item(restaurant_id, item_id)