from pathlib import Path
import csv
from typing import Dict, Any
# pylint: disable=duplicate-code

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "menuItems.csv"

def load_menu(restaurant_id: int) -> Dict[Any, Dict[Any, Any]]:
    if not DATA_PATH.exists():
        raise FileExistsError(
            "Error: The storage csv does not exist or otherwise cannot be accessed"
            )
    with DATA_PATH.open("r", encoding="utf-8", newline='') as f:
        reader = csv.DictReader(f, delimiter=',')
        items = {}
        for row in reader:
            if (int(row["restaurant_id"]) == restaurant_id):
                items[row["restaurant_id"]] = row
                items[row["item_id"]].pop("restaurant_id")
        return items
    
def load_menu_item(restaurant_id: int, item_id: int) -> Dict[Any, Any]:
    if not DATA_PATH.exists():
        raise FileExistsError(
            "Error: The storage csv does not exist or otherwise cannot be accessed"
            )
    with DATA_PATH.open("r", encoding="utf-8", newline='') as f:
        reader = csv.DictReader(f, delimiter=',')
        for row in reader:
            if (int(row["restaurant_id"]) == restaurant_id and int(row["item_id"]) == item_id):
                return row
        raise IndexError(f"Error: Unable to find item id:{item_id} belonging to restaurant id:{restaurant_id}")

def save_menu(restaurant_id: int, items: Dict[Any, Dict[Any, Any]]) -> None:
    fieldNames = ['restaurant_id','item_id','item_name','price','description','image']
    with DATA_PATH.open("w", encoding="utf-8", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldNames)
        writer.writeheader()
        for row in items:
            row['restaurant_id'] = restaurant_id
            writer.writerow(row)
