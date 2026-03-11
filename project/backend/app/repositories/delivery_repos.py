#defines reading and writing data, handles NO BUISNESS LOGIC.
# NEED TO DECIDE HOW TO STORE DATA

from pathlib import Path
import csv, os
from typing import Dict, Any

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "food_delivery.csv"

#Returnes a list of dicts where each dict maps to an order
def load_all_deliveries() -> Dict[Dict[Any]]:
    if not DATA_PATH.exists():
        return []
    with DATA_PATH.open("r", encoding="utf-8", newline='') as f:
        #TODO: Load specific data from csv, create storage and related methods for other classes
        reader = csv.DictReader(f, delimiter=',')
        orders = {}
        #TODO:Add data validation
        for row in reader:
            orders[row.get("order_id")] = row
        return orders

def load_specific_delivery(orderId: str) -> Dict[Any]:
    if not DATA_PATH.exists():
        return []
    with DATA_PATH.open("r", encoding="utf-8", newline='') as f:
        reader = csv.DictReader(f, delimiter=',')
        for row in reader:
            if row.get("order_id") == orderId:
                return row
        return []

def save_all_deliveries(deliveries: Dict[Dict[Any]]) -> None:
    tmp = DATA_PATH.with_suffix(".tmp")
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
    with tmp.open("w", encoding="utf-8", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=field_names)
        writer.writeheader()
        for row in deliveries:
            writer.writerow(row)
        os.replace(tmp, DATA_PATH)
