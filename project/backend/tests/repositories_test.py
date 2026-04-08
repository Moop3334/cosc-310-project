# pylint: disable=unused-wildcard-import
# pylint: disable=wildcard-import
# pylint: disable=unused-import
import pytest
from fastapi import HTTPException
from app.repositories.delivery_repos import (
    load_all_deliveries,
    load_specific_delivery,
    save_all_deliveries,
)
from app.repositories import (
    save_all_restaurants,
    load_all_restaurants,
    load_menu,
    load_menu_item,
    save_menu,
    load_all_order,
    save_all_orders
)
from app.schema.order import Order
from app.services.order_service import dict_to_order

test_delivery_1 = {
    'order_id': '154b2cZ', 
    'restaurant_id': '72', 
    'food_item': 'Cookie', 
    'order_time': '2024-06-15', 
    'delivery_time': '2024-06-15', 
    'delivery_distance': '4.94', 
    'order_value': '20.83', 
    'delivery_method': 'Walk', 
    'traffic_condition': 'High', 
    'weather_condition': 'Sunny', 
    'delivery_time_actual': '0.0', 
    'delivery_delay': '7.7', 
    'route_taken': 'Route_3', 
    'customer_id': 'd0125022-ae80-451f-91c6-17cb18f1224a', 
    'age': '57', 
    'gender': 'Female', 
    'location': 'City_3', 
    'order_history': '41', 
    'customer_rating': '2', 
    'preferred_cuisine': 'Mexican', 
    'order_frequency': 'Monthly', 
    'loyalty_program': 'No', 
    'food_temperature': 'Cold', 
    'food_freshness': '2', 
    'packaging_quality': '5', 
    'food_condition': 'Good', 
    'customer_satisfaction': '1', 
    'small_route': 'False', 
    'bike_friendly_route': 'False', 
    'route_type': 'Mixed', 
    'route_efficiency': '0.09812902009060986', 
    'predicted_delivery_mode': 'Car', 
    'traffic_avoidance': 'No'
}

test_delivery_2 = {
    'order_id': '154b2cz', 
    'restaurant_id': '72', 
    'food_item': 'Cookie', 
    'order_time': '2024-06-15', 
    'delivery_time': '2024-06-15', 
    'delivery_distance': '4.94', 
    'order_value': '20.83', 
    'delivery_method': 'Walk', 
    'traffic_condition': 'High', 
    'weather_condition': 'Sunny', 
    'delivery_time_actual': '0.0', 
    'delivery_delay': '7.7', 
    'route_taken': 'Route_3', 
    'customer_id': 'd0125022-ae80-451f-91c6-17cb18f1224a', 
    'age': '57', 
    'gender': 'Female', 
    'location': 'City_3', 
    'order_history': '41', 
    'customer_rating': '2', 
    'preferred_cuisine': 'Mexican', 
    'order_frequency': 'Monthly', 
    'loyalty_program': 'No', 
    'food_temperature': 'Cold', 
    'food_freshness': '2', 
    'packaging_quality': '5', 
    'food_condition': 'Good', 
    'customer_satisfaction': '1', 
    'small_route': 'False', 
    'bike_friendly_route': 'False', 
    'route_type': 'Mixed', 
    'route_efficiency': '0.09812902009060986', 
    'predicted_delivery_mode': 'Car', 
    'traffic_avoidance': 'No'
}

test_menu_item = {
    'restaurant_id': '1', 
    'id': '1', 
    'item_name': 'Curry', 
    'price': '12.99', 
    'description': 'Japanese Curry'
}

test_menu1 = [
    {
        'restaurant_id':'1',
        'id': '1',
        'item_name': 'Curry', 
        'price': '12.99', 
        'description': 'Japanese Curry'
        }, 
    {
        'restaurant_id':'1',
        'id': '2',
        'item_name': 'Chicken', 
        'price': '10.0', 
        'description': 'Mmmm chicken'
    }
]

test_menu2 = [
    {
        'restaurant_id':'2',
        'id': '1',
        'item_name': 'Curry', 
        'price': '12.99', 
        'description': 'Japanese Curry'
        }, 
    {
        'restaurant_id':'2',
        'id': '2',
        'item_name': 'Chicken', 
        'price': '10.0', 
        'description': 'Mmmm chicken'
    }
]

test_restaurant1 = {
    "id":"1", 
    "name":"Tester's Dinner", 
    "address":"123 Road dr", 
    "open_times":['09:00:00', '09:00:00', '09:00:00', '09:00:00', '09:00:00', '09:00:00', '09:00:00'], 
    "close_times":['21:00:00', '21:00:00', '21:00:00', '21:00:00', '21:00:00', '21:00:00', '21:00:00'],
    'menu':test_menu1
}

test_restaurant2 = {
    "id":"2", 
    "name":"Example Kitchen", 
    "address":"124 Road dr", 
    "open_times":['09:00:00', '09:00:00', '09:00:00', '09:00:00', '09:00:00', '09:00:00', '09:00:00'], 
    "close_times":['21:00:00', '21:00:00', '21:00:00', '21:00:00', '21:00:00', '21:00:00', '21:00:00'],
    'menu':test_menu2
}

test_order_1 = {
    "id":"1",
    "user_id":"1",
    "restaurant_id":"1",
    "items":[{"item_id": 1, "item_name": "Curry", "quantity": 1, "price": 12.99}],
    "total_price":12.99,
    "creation_date":"2026-01-01 12:00:00",
    "status":"Pending Approval"
}
test_order_2 = {
    "id":"10",
    "user_id":"9",
    "restaurant_id":"9",
    "items":[{"item_id": 2, "item_name": "Cookie", "quantity": 1, "price": 2.99}],
    "total_price":2.99,
    "creation_date":"2026-01-01 13:00:00",
    "status":"Pending Approval"
}

def test_order_load():
    orders = load_all_order()
    order = {}
    for row in orders:
        if row.get("id") == test_order_1["id"]:
            order = row
    # Compare required fields since items is stored as JSON string
    assert order.get("id") == test_order_1["id"]
    assert order.get("user_id") == test_order_1["user_id"]
    assert order.get("restaurant_id") == test_order_1["restaurant_id"]
    assert order.get("total_price") == test_order_1["total_price"]
    assert order.get("status") == test_order_1["status"]

def test_order_save():
    orders = load_all_order()
    orders = [dict_to_order(o) for o in orders]
    orders.append(dict_to_order(test_order_2))
    save_all_orders(orders)
    o = load_all_order()
    hasMatch = False
    for row in o:
        # Compare required fields since items is stored as JSON string
        if (row.get("id") == test_order_2["id"] and 
            row.get("user_id") == test_order_2["user_id"] and
            row.get("restaurant_id") == test_order_2["restaurant_id"] and
            row.get("total_price") == test_order_2["total_price"] and
            row.get("status") == test_order_2["status"]):
            hasMatch = True
    assert hasMatch

def test_delivery_load():
    deliveries = load_all_deliveries()
    order = {}
    for row in deliveries:
        if row["order_id"] == test_delivery_1["order_id"]:
            order = row
    assert order == test_delivery_1
    

def test_single_delivery_load():
    delivery = load_specific_delivery("154b2cZ")
    assert delivery == test_delivery_1

def test_delivery_save():
    deliveries = load_all_deliveries()
    deliveries.append(test_delivery_2)
    save_all_deliveries(deliveries)
    d = load_all_deliveries()
    hasMatch = False
    for row in d:
        hasMatch = row == test_delivery_2
    assert hasMatch

def test_restaurant_load():
    restaurants = load_all_restaurants()
    assert restaurants[1] == test_restaurant2

def test_restaurant_save():
    restaurants = load_all_restaurants()
    restaurants[1] = test_restaurant2
    save_all_restaurants(restaurants)
    r = load_all_restaurants()
    assert r[1] == test_restaurant2

def test_load_menu_item_error():
    with pytest.raises(HTTPException):
        load_menu_item(100,3)

def test_load_menu_error():
    with pytest.raises(HTTPException):
        load_menu(100)

def test_load_menu_item():
    item = load_menu_item(1,1)
    assert item == test_menu_item

def test_load_menu():
    menu = load_menu(2)
    assert menu == test_menu2

def test_save_menu():
    save_menu(2,test_menu2)
    temp_menu = load_menu(2)
    assert temp_menu == test_menu2
