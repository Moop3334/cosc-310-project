from typing import List
import pytest
from fastapi import HTTPException
from app.schema.resturant import Restaurant, RestaurantCreate, RestaurantUpdate
from app.schema.menuItems import MenuItem, MenuItemCreate, MenuItemUpdate
from app.repositories.restaurant_repos import save_all_restaurants
from app.repositories.menu_items_repos import save_menu
from app.services.restaurant_service import list_restaurants, create_restaurant, get_restaurant_by_id, update_restaurant, delete_restaurant
from app.services.menu_service import list_menu, get_menu_item_by_id, create_menu_item, update_menu_item, delete_menu_item

test_menu1 = [
    MenuItem(
        id=1,
        restaurant_id=1,
        item_name="Curry",
        price=12.99,
        description="Japanese Curry",
        image="N/A"
    ),
    MenuItem(
        id=2,
        restaurant_id=1,
        item_name="Chicken",
        price=10,
        description="Mmmm chicken",
        image="N/A"
    )
]
test_menu2 = [
    MenuItem(
        id=1,
        restaurant_id=2,
        item_name="Curry",
        price=12.99,
        description="Japanese Curry",
        image="N/A"
    ),
    MenuItem(
        id=2,
        restaurant_id=2,
        item_name="Chicken",
        price=10,
        description="Mmmm chicken",
        image="N/A"
    )
]
test_menu3 = [
    MenuItem(
        id=1,
        restaurant_id=3,
        item_name="Curry",
        price=12.99,
        description="Japanese Curry",
        image="N/A"
    ),
    MenuItem(
        id=2,
        restaurant_id=3,
        item_name="Chicken",
        price=10,
        description="Mmmm chicken",
        image="N/A"
    )
]
test_menu4 = [
    MenuItem(
        id=1,
        restaurant_id=4,
        item_name="Curry",
        price=12.99,
        description="Japanese Curry",
        image="N/A"
    ),
    MenuItem(
        id=2,
        restaurant_id=4,
        item_name="Chicken",
        price=10,
        description="Mmmm chicken",
        image="N/A"
    )
]

test_restaurants = List[Restaurant]
test_restaurants = [
    Restaurant(
        id=1,
        name="Tester's Dinner",
        address="123 Road dr",
        open_times=[
            "09:00:00",
            "09:00:00",
            "09:00:00",
            "09:00:00",
            "09:00:00",
            "09:00:00",
            "09:00:00"
        ],
        close_times=[
            "21:00:00",
            "21:00:00",
            "21:00:00",
            "21:00:00",
            "21:00:00",
            "21:00:00",
            "21:00:00"
        ],
        menu=test_menu1
    ),
    Restaurant(
        id=2,
        name="Example Kitchen",
        address="124 Road dr",
        open_times=[
            "09:00:00",
            "09:00:00",
            "09:00:00",
            "09:00:00",
            "09:00:00",
            "09:00:00",
            "09:00:00"
        ],
        close_times=[
            "21:00:00",
            "21:00:00",
            "21:00:00",
            "21:00:00",
            "21:00:00",
            "21:00:00",
            "21:00:00"
        ],
        menu=test_menu2
    ),
    Restaurant(
        id=3,
        name="Foo Bar",
        address="999 Pun St",
        open_times=[
            "09:00:00",
            "09:00:00",
            "09:00:00",
            "09:00:00",
            "09:00:00",
            "09:00:00",
            "09:00:00"
        ],
        close_times=[
            "21:00:00",
            "21:00:00",
            "21:00:00",
            "21:00:00",
            "21:00:00",
            "21:00:00",
            "21:00:00"
        ],
        menu=test_menu3
    )
]

test_restaurant_create = RestaurantCreate(
    name="Papa Louie's Pizzaria",
    address="2004 Cool Math blvd",
    open_times=[
        "09:00:00",
        "09:00:00",
        "09:00:00",
        "09:00:00",
        "09:00:00",
        "09:00:00",
        "09:00:00"
    ],
    close_times=[
        "21:00:00",
        "21:00:00",
        "21:00:00",
        "21:00:00",
        "21:00:00",
        "21:00:00",
        "21:00:00"
    ],
    menu=test_menu4
)
test_restaurant_update = RestaurantUpdate(
    name="Tester's Dinner",
    address="123 Road Dr",
    open_times=[
        "09:00:00",
        "09:00:00",
        "09:00:00",
        "09:00:00",
        "09:00:00",
        "09:00:00",
        "09:00:00"
    ],
    close_times=[
        "21:00:00",
        "21:00:00",
        "21:00:00",
        "21:00:00",
        "21:00:00",
        "21:00:00",
        "21:00:00"
    ],
    menu=test_menu1
)

save_all_restaurants(test_restaurants)

def test_list_restaurants():
    assert test_restaurants == list_restaurants()

def test_create_restaurant():
    tmp_restaurant = create_restaurant(test_restaurant_create)
    assert tmp_restaurant == list_restaurants()[3]

def test_delete_restaurant():
    try:
        delete_restaurant(4)
    except HTTPException:
        pytest.fail("Restaurant does not exist")

def test_delete_invalid_id():
    with pytest.raises(HTTPException):
        delete_restaurant(100)

def test_get_restaurant_by_id():
    assert test_restaurants[1] == get_restaurant_by_id(2)

def test_get_invalid_restaurant_id():
    with pytest.raises(HTTPException):
        get_restaurant_by_id(100)

def test_update_restaurant():
    test_restaurants[0] = update_restaurant(1, test_restaurant_update)
    assert test_restaurants[0] == list_restaurants()[0]

def test_update_invalid_restaurant_id():
    with pytest.raises(HTTPException):
        update_restaurant(100, test_restaurant_update)