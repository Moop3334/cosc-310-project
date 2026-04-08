from pathlib import Path
import csv
from fastapi import HTTPException
from typing import Dict, Any, List
# pylint: disable=duplicate-code

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "menu_items.csv"

def load_menu(restaurant_id: int) -> List[Dict[Any, Any]]:
    if not DATA_PATH.exists():
        raise FileExistsError(
            "Error: The storage csv does not exist or otherwise cannot be accessed"
            )
    with DATA_PATH.open("r", encoding="utf-8", newline='') as f:
        reader = csv.DictReader(f, delimiter=',')
        items = []
        for row in reader:
            if (int(row["restaurant_id"]) == restaurant_id):
                items.append(row)
        if (len(items) > 0):
            return items
        else:
            raise HTTPException(status_code=404, detail=f"Unable to find a restaurant with id {restaurant_id}")
        
def load_menu_item(restaurant_id: int, item_id: int) -> Dict[Any, Any]:
    if not DATA_PATH.exists():
        raise FileExistsError(
            "Error: The storage csv does not exist or otherwise cannot be accessed"
            )
    with DATA_PATH.open("r", encoding="utf-8", newline='') as f:
        reader = csv.DictReader(f, delimiter=',')
        for row in reader:
            if (int(row["restaurant_id"]) == restaurant_id and int(row["id"]) == item_id):
                return row
        raise HTTPException(status_code=404, detail=f"Error: Unable to find item id:{item_id} belonging to restaurant id:{restaurant_id}")

def save_menu(restaurant_id: int, items: List[Dict[Any, Any]]) -> None:
    fieldNames = ['restaurant_id','id','item_name','price','description']
    if not DATA_PATH.exists():
        raise FileExistsError(
            "Error: The storage csv does not exist or otherwise cannot be accessed"
            )

    existing_rows = []
    with DATA_PATH.open("r", encoding="utf-8", newline='') as f:
        reader = csv.DictReader(f)
        existing_rows = list(reader)
    existing_rows = [row for row in existing_rows if row.get("restaurant_id") != str(restaurant_id)]

    with DATA_PATH.open("w", encoding="utf-8", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldNames)
        writer.writeheader()
        new_rows = []
        for row in items:
            row = dict(row)
            row["restaurant_id"] = restaurant_id
            new_rows.append(row)
        writer.writerows(existing_rows + new_rows)
            