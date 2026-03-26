from types import NoneType
from typing import List
import re
import datetime
from fastapi import HTTPException
from app.schema.resturant import Restaurant, RestaurantCreate, RestaurantUpdate
from app.schema.menuItems import MenuItem, MenuItemCreate, MenuItemUpdate
from app.services.menu_service import create_menu_item, delete_menu_item
from app.repositories.restaurant_repos import load_all_restaurants, save_all_restaurants

def list_restaurants() -> List[Restaurant]:
    r_list = []
    for r in load_all_restaurants():
        opn_list = [datetime.time.strptime(it, "%H:%M:%S") for it in r.get("open_times")]
        close_list = [datetime.time.strptime(it, "%H:%M:%S") for it in r.get("close_times")]
        menu = []
        for m in r.get("menu"):
            menu.append(MenuItem(
                id = m.get("id"),
                restaurant_id= r.get("id"),
                item_name = m.get("item_name"),
                price = m.get("price"),
                description=m.get("description"),
                image=m.get("image")
            ))
        r_list.append(
            Restaurant(
            id=r.get("id"),
            name=r.get("name"),
            address=r.get("address"),
            open_times=opn_list,
            close_times=close_list,
            menu=menu
            ))
    return r_list

def create_restaurant(payload: RestaurantCreate) -> Restaurant:
    items = load_all_restaurants() #make sure all data types in payload are correct
    for r in items:
        if r.get("name") == payload.name.strip() and r.get("address") == payload.address.strip():
            raise HTTPException(status_code=409, detail=f"Restaurant Already Exists")
    new_id = len(items) + 1
    new_menu = []
    for m in payload.menu:
        new_menu.append(create_menu_item(new_id, MenuItemCreate(
            item_name=m.item_name,
            restaurant_id=new_id,
            price=m.price,
            description=m.description,
            image=m.image
        )))
    new_item = Restaurant(id=new_id, name=payload.name.strip(), address=payload.address.strip(), open_times=payload.open_times, close_times=payload.close_times, menu=new_menu)
    items.append(new_item.model_dump())
    save_all_restaurants(items)
    return new_item

def get_restaurant_by_id(restaurant_id: int) -> Restaurant:
    items = list_restaurants()
    for it in items:
        if it.id == restaurant_id:
            return it
    raise HTTPException(status_code=404, detail=f"Restaurant '{restaurant_id}' not found")

def update_restaurant(restaurant_id: int, payload: RestaurantUpdate) -> Restaurant:
    items = list_restaurants() #make sure all data types in payload are correct
    for idx, it in enumerate(items):
        if it.id == restaurant_id:
            updated = Restaurant(
                id=restaurant_id, 
                name=payload.name.strip(), 
                address=payload.address.strip(), 
                open_times=payload.open_times, 
                close_times=payload.close_times,
                menu=payload.menu
            )
            items[idx] = updated.model_dump()
            save_all_restaurants(items)
            return updated
    raise HTTPException(status_code=404, detail=f"Restaurant '{restaurant_id}' not found")

def delete_restaurant(restaurant_id: int) -> None:
    items = list_restaurants()
    new_items = [it for it in items if it.id != restaurant_id]
    for r in items:
        if r.id == restaurant_id:
            for m in r.menu:
                delete_menu_item(r.id, m.id)
    if len(new_items) == len(items):
        raise HTTPException(status_code=404, detail=f"Restaurant '{restaurant_id}' not found")
    save_all_restaurants(new_items)

def filter_restaurants(search: str):
    restaurants = list_restaurants()
    r_matches = []
    for r in restaurants:
        m = re.search(search, r.name, re.IGNORECASE)
        if type(m) is not NoneType:
            r_matches.append(r)
    return r_matches