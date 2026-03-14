# pylint: disable=unused-wildcard-import
# pylint: disable=wildcard-import
# pylint: disable=unused-import
import pytest
from app.repositories import (
    load_all_deliveries,
    load_specific_delivery,
    save_all_deliveries,
    save_all_restaurants,
    load_all_restaurants,
    load_menu,
    load_menu_item,
    save_menu
)

test_order_1 = {
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

test_order_2 = {
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

test_restaurant1 = {
    "restaurant_id":"1", 
    "restaurant_name":"Tester's Dinner", 
    "address":"123 Road dr", 
    "open_times":['9:00', '9:00', '9:00', '9:00', '9:00', '9:00', '9:00'], 
    "close_times":['21:00', '21:00', '21:00', '21:00', '21:00', '21:00', '21:00'],
}

test_restaurant2 = {
    "restaurant_id":"2", 
    "restaurant_name":"Example Kitchen", 
    "address":"124 Road dr", 
    "open_times":['9:00', '9:00', '9:00', '9:00', '9:00', '9:00', '9:00'], 
    "close_times":['21:00', '21:00', '21:00', '21:00', '21:00', '21:00', '21:00'],
}

test_menu_item = {
    'restaurant_id': '1', 
    'item_id': '1', 
    'item_name': 'Curry', 
    'price': '12.99', 
    'description': 'Japanese Curry', 
    'image': 'N/A'
}

test_menu = {
    '1': {
        'item_id': '1',
        'item_name': 'Curry', 
        'price': '12.99', 
        'description': 'Japanese Curry', 
        'image': 'N/A'
        }, 
    '2': {
        'item_id': '2',
        'item_name': 'Chicken', 
        'price': '10.00', 
        'description': 'Mmmm chicken', 
        'image': 'N/A'
    }
}

def test_delivery_load():
    deliveries = load_all_deliveries()
    assert deliveries["154b2cZ"] == test_order_1

def test_single_delivery_load():
    delivery = load_specific_delivery("154b2cZ")
    assert delivery == test_order_1

def test_delivery_save():
    deliveries = load_all_deliveries()
    deliveries["154b2cz"] = test_order_2
    save_all_deliveries(deliveries)
    d = load_all_deliveries()
    assert d["154b2cz"] == test_order_2

def test_restaurant_load():
    restaurants = load_all_restaurants()
    assert restaurants[0] == test_restaurant1

def test_restaurant_save():
    restaurants = load_all_restaurants()
    restaurants[1] = test_restaurant2
    save_all_restaurants(restaurants)
    r = load_all_restaurants()
    assert r[1] == test_restaurant2

def test_load_menu_item_error():
    with pytest.raises(IndexError):
        load_menu_item(100,3)

def test_load_menu_error():
    with pytest.raises(IndexError):
        load_menu(100)

def test_load_menu_item():
    item = load_menu_item(1,1)
    assert item == test_menu_item

def test_load_menu():
    menu = load_menu(1)
    assert menu == test_menu

def test_save_menu():
    save_menu(3,test_menu)
    temp_menu = load_menu(3)
    assert test_menu == test_menu