import uuid
from typing import List, Dict, Any
import datetime
from fastapi import HTTPException
from app.schema.resturant import Restaurant, RestaurantCreate, RestaurantUpdate
from app.schema.menuItems import MenuItem, MenuItemCreate, MenuItemUpdate
from app.repositories.restaurant_repos import load_all_restaurants, save_all_restaurants

def list_restaurants() -> List[Restaurant]:
    r_list = []
    for r in load_all_restaurants():
        opn_list = [datetime.time.strptime(it, "%H:%M") for it in r.get("open_times")]
        close_list = [datetime.time.strptime(it, "%H:%M") for it in r.get("close_times")]
        menu = []
        for m in r.get("menu"):
            menu.append(MenuItem(
                id = m.get("item_id"),
                name = m.get("item_name"),
                price = m.get("price"),
                description=m.get("description"),
                image=m.get("image")
            ))
        r_list.append(
            Restaurant(
            id=r.get("restaurant_id"),
            name=r.get("restaurant_name"),
            address=r.get("address"),
            openTimes=opn_list,
            closeTimes=close_list,
            menu=menu
            ))
    return r_list

def create_restaurant(payload: RestaurantCreate) -> Restaurant:
    items = ListRestaurants()
    new_id = len(items)
    new_item = Restaurant(id=new_id, name=payload.name.strip(), address=payload.address.strip(), openTimes=payload.openTimes.strip(), closeTimes=payload.closeTimes.strip(), menu=payload.menu.strip())
    items.append(new_item.dict())
    save_all_restaurants(items)
    return new_item

def get_restaurant_by_id(restaurant_id: str) -> Restaurant:
    items = ListRestaurants()
    for it in items:
        if it.id == restaurant_id:
            return Restaurant(**it)
    raise HTTPException(status_code=404, detail=f"Restaurant '{restaurant_id}' not found")

def update_restaurant(restaurant_id: str, payload: RestaurantUpdate) -> Restaurant:
    items = ListRestaurants()
    for idx, it in enumerate(items):
        if it.id == restaurant_id:
            updated = Restaurant(
                id=restaurant_id, 
                name=payload.name.strip(), 
                address=payload.address.strip(), 
                openTimes=payload.openTimes.strip(), 
                closeTimes=payload.closeTimes.strip(),
                menu=payload.menu.strip()
            )
            items[idx] = updated.dict()
            save_all_restaurants(items)
            return updated
    raise HTTPException(status_code=404, detail=f"Restaurant '{restaurant_id}' not found")

def delete_restaurant(restaurant_id: str) -> None:
    items = ListRestaurants
    new_items = [it for it in items if it.id != restaurant_id]
    if len(new_items) == len(items):
        raise HTTPException(status_code=404, detail=f"Restaurant '{restaurant_id}' not found")
    save_all_restaurants(new_items)
