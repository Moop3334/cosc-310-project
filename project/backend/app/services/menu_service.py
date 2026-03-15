from typing import List
from fastapi import HTTPException
from app.schema.menuItems import MenuItem, MenuItemCreate, MenuItemUpdate
from app.repositories.menu_items_repos import load_menu, save_menu

def list_menu(restaurant_id: int) -> List[MenuItem]:
    m_list = []
    menu = load_menu(restaurant_id)
    for m in menu:
        m_list.append(MenuItem(
                item_id = m.get("item_id"),
                restaurant_id= restaurant_id,
                item_name = m.get("item_name"),
                price = m.get("price"),
                description=m.get("description"),
                image=m.get("image")
            ))
    return m_list

def create_menu_item(payload: MenuItemCreate) -> MenuItem:
    items = list_menu(restaurant_id=payload.restaurant_id)
    new_id = len(items) + 1
    new_item = MenuItem(
        item_id=new_id, 
        restaurant_id=payload.restaurant_id, 
        item_name=payload.item_name.strip(), 
        price=payload.price, 
        description=payload.description.strip(), 
        image=payload.image.strip()
    )
    items.append(new_item.dict())
    save_menu(items)
    return new_item

def get_menu_item_by_id(restaurant_id: int, item_id: int) -> MenuItem:
    items = list_menu(restaurant_id)
    for it in items:
        if it.item_id == item_id:
            return it
    raise HTTPException(status_code=404, detail=f"Menu Item '{item_id}' not found for restaurant {restaurant_id}")

def update_menu_item(item_id: int, payload: MenuItemUpdate) -> MenuItem:
    items = list_menu(payload.restaurant_id)
    for idx, it in enumerate(items):
        if it.item_id == item_id:
            updated = MenuItem(
                item_id=item_id,
                restaurant_id=payload.restaurant_id,
                item_name=payload.item_name.strip(),
                price=payload.price,
                description=payload.description,
                image=payload.image
            )
            items[idx] = updated.dict()
            save_menu(payload.restaurant_id,items)
            return updated
    raise HTTPException(status_code=404, detail=f"Menu Item '{item_id}' not found for restaurant {payload.restaurant_id}")

def delete_menu_item(restaurant_id: int, item_id: int) -> None:
    items = list_menu(restaurant_id=restaurant_id)
    new_items = [it for it in items if it.item_id != item_id]
    if len(new_items) == len(items):
        raise HTTPException(status_code=404, detail=f"Menu Item '{item_id}' not found for restaurant {restaurant_id}")
    save_menu(restaurant_id, new_items)
