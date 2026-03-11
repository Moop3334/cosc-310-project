from pathlib import Path
import csv, os
from typing import List, Dict, Any

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "restaurants.csv"

#Returnes a list of dicts where each dict maps to an order
def load_all_restaurants() -> Dict[Dict[Any]]:
   if not DATA_PATH.exists():
       return []
   with DATA_PATH.open("r", encoding="utf-8", newline='') as f:
       #TODO: Load specific data from csv, create csv and related methods for other classes
       reader = csv.DictReader(f, delimiter=',')
       orders = {}
       #TODO:Add data validation
       for row in reader:
           orders[row.get("restaurant_id")] = row
           #TODO: Implement the ability to parse arrays/lists for the open/closing times and menu
       return orders

def save_all_restaurants(deliveries: Dict[Dict[Any]]) -> None:
    tmp = DATA_PATH.with_suffix(".tmp")
    fieldNames = ['restaurant_id','restaurant_name','address','open_times','close_times','menu']
    with tmp.open("w", encoding="utf-8", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldNames)
        writer.writeheader()
        for row in deliveries:
            writer.writerow(row)
        os.replace(tmp, DATA_PATH)