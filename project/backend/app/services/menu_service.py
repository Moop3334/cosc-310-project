from types import NoneType
from typing import List
import re
from fastapi import HTTPException
from app.schema.menu_items import MenuItem, MenuItemCreate, MenuItemUpdate
from app.repositories.menu_items_repos import load_menu, save_menu

def list_menu(restaurant_id: int) -> List[MenuItem]:
    m_list = []
    menu = load_menu(restaurant_id)
    for m in menu:
        m_list.append(MenuItem(
                id = m.get("id"),
                restaurant_id= restaurant_id,
                item_name = m.get("item_name"),
                price = m.get("price"),
                description=m.get("description"),
                image=m.get("image")
            ))
    return m_list

def create_menu_item(restaurant_id: int, payload: MenuItemCreate) -> MenuItem:
    items = List[MenuItem]
    try:
        items = list_menu(restaurant_id=restaurant_id)
    except HTTPException:
        items = []
    new_id = len(items) + 1
    new_item = MenuItem(
        id=new_id, 
        restaurant_id=restaurant_id, 
        item_name=payload.item_name.strip(), 
        price=payload.price, 
        description=payload.description.strip(), 
        image=payload.image.strip()
    )
    items.append(new_item.model_dump())
    save_menu(restaurant_id,items)
    return new_item

def get_menu_item_by_id(restaurant_id: int, item_id: int) -> MenuItem:
    items = list_menu(restaurant_id)
    for it in items:
        if it.id == item_id:
            return it
    raise HTTPException(status_code=404, detail=f"Menu Item {item_id} not found for restaurant {restaurant_id}")

def update_menu_item(restaurant_id: int, item_id: int, payload: MenuItemUpdate) -> MenuItem:
    items = list_menu(restaurant_id) #Make sure all data types in the payload are correct
    for idx, it in enumerate(items):
        if it.id == item_id:
            updated = MenuItem(
                id=item_id,
                restaurant_id=restaurant_id,
                item_name=payload.item_name.strip(),
                price=payload.price,
                description=payload.description,
                image=payload.image
            )
            items[idx] = updated.model_dump()
            save_menu(payload.restaurant_id,items)
            return updated
    raise HTTPException(status_code=404, detail=f"Menu Item {item_id} not found for restaurant {payload.restaurant_id}")

def delete_menu_item(restaurant_id: int, item_id: int) -> None:
    items = list_menu(restaurant_id=restaurant_id)
    new_items = [it for it in items if it.id != item_id]
    if len(new_items) == len(items):
        raise HTTPException(status_code=404, detail=f"Menu Item {item_id} not found for restaurant {restaurant_id}")
    save_menu(restaurant_id, new_items)

def filter_menu_items(restaurant_id: int, search: str):
    items = list_menu(restaurant_id)
    r_matches = []
    for it in items:
        m = re.search(search, it.item_name, re.IGNORECASE)
        if type(m) is not NoneType:
            r_matches.append(it)
    return r_matches