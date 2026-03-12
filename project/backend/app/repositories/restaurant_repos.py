from pathlib import Path
import csv, os
from typing import Dict, Any
# pylint: disable=duplicate-code

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "restaurants.csv"

#Returnes a list of dicts where each dict maps to an order
def load_all_restaurants() -> Dict[Dict[Any]]:
    if not DATA_PATH.exists():
        raise FileExistsError(
            "Error: The storage csv does not exist or otherwise cannot be accessed"
            )
    with DATA_PATH.open("r", encoding="utf-8", newline='') as f:
        reader = csv.DictReader(f, delimiter=',')
        orders = {}
        for row in reader:
            orders[row.get("restaurant_id")] = row
           #TODO: Implement the ability to parse arrays/lists for the open/closing times and menu
        return orders

def save_all_restaurants(restaurants: Dict[Dict[Any]]) -> None:
    fieldNames = ['restaurant_id','restaurant_name','address','open_times','close_times','menu']
    with DATA_PATH.open("w", encoding="utf-8", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldNames)
        writer.writeheader()
        restaurants_temp = []
        for row in restaurants:
            restaurants_temp.append(restaurants[row])
        writer.writerows(restaurants_temp)
