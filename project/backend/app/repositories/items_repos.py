#defines reading and writing data, handles NO BUISNESS LOGIC.
# NEED TO DECIDE HOW TO STORE DATA

from pathlib import Path
import csv, os
from typing import List, Dict, Any

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "food_delivery.csv"

#Returnes a list of dicts where each dict maps to an order
def load_all_deliveries() -> List[Dict[Any]]:
   if not DATA_PATH.exists():
       return []
   with DATA_PATH.open("r", encoding="utf-8", newline='') as f:
       #TODO: Load specific data from csv
       reader = csv.DictReader(f, delimiter=',')
       orders = {}
       #TODO:Add date class for validation
       for row in reader:
           orders[row.get("order_id")] = row
       return orders

def save_all(items: List[Dict[str, Any]]) -> None:
    tmp = DATA_PATH.with_suffix(".tmp")
    with tmp.open("w", encoding="utf-8") as f:
        #json.dump(items, f, ensure_ascii=False, indent=2)
        os.replace(tmp, DATA_PATH)