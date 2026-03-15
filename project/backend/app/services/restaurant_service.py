import uuid
from typing import List, Dict, Any
from fastapi import HTTPException
from app.schema.resturant import Restaurant, RestaurantCreate, RestaurantUpdate
from app.schema.menuItems import MenuItem, MenuItemCreate, MenuItemUpdate
from repositories.restaurant_repos import load_all_restaurants, save_all_restaurants

def ListRestaurants() -> List[Restaurant]:
    return [Restaurant(**it) for it in load_all_restaurants()]

print(ListRestaurants())
