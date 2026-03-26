#defines reading and writing data, handles NO BUISNESS LOGIC.

from pathlib import Path
import csv#, os
from typing import Dict,Any,List

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "food_delivery.csv"

#Returnes a list of dicts where each dict maps to an order
def load_all_deliveries() -> List[Dict[Any, Any]]:
    if not DATA_PATH.exists():
        raise FileExistsError(
            "Error: The storage csv does not exist or otherwise cannot be accessed"
            )
    with DATA_PATH.open("r", encoding="utf-8", newline='') as f:
        reader = csv.DictReader(f, delimiter=',')
        orders = []
        for row in reader:
            orders.append(row)
        return orders

def load_specific_delivery(orderId: str) -> Dict[Any, Any]:
    if not DATA_PATH.exists():
        raise FileExistsError(
            "Error: The storage csv does not exist or otherwise cannot be accessed"
            )
    with DATA_PATH.open("r", encoding="utf-8", newline='') as f:
        reader = csv.DictReader(f, delimiter=',')
        for row in reader:
            if row.get("order_id") == orderId:
                return row
        raise IndexError(f"Error: The order with Id {orderId} cannot be found")

def save_all_deliveries(deliveries: List[Dict[Any, Any]]) -> None:
    field_names = [
        "order_id","restaurant_id","food_item",
        "order_time","delivery_time","delivery_distance",
        "order_value",'delivery_method','traffic_condition',
        'weather_condition','delivery_time_actual','delivery_delay',
        'route_taken','customer_id','age','gender','location','order_history',
        'customer_rating','preferred_cuisine','order_frequency','loyalty_program',
        'food_temperature','food_freshness','packaging_quality','food_condition',
        'customer_satisfaction','small_route','bike_friendly_route','route_type',
        'route_efficiency','predicted_delivery_mode','traffic_avoidance'
        ]
    with DATA_PATH.open("w", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=field_names)
        writer.writeheader()
        orders_temp = []
        for row in deliveries:
            orders_temp.append(row)
        writer.writerows(orders_temp)

def save_a_delivery(new_delivery: Dict[Any, Any]) -> str:
    deliveries = load_all_deliveries()
    deliveries.append(new_delivery)
    save_all_deliveries(deliveries)
    return f"Delivery with order id {new_delivery.get('order_id')} created successfully."