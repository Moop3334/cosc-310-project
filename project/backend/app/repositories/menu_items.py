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

def save_all_restaurants(restaurants: Dict[Any, Dict[Any, Any]]) -> None:
    fieldNames = ['restaurant_id','restaurant_name','address','open_times','close_times','menu_id']
    with DATA_PATH.open("w", encoding="utf-8", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldNames)
        writer.writeheader()
        restaurants_temp = []
        open_tmp = []
        close_tmp = []
        for row in restaurants:
            opn = restaurants[row]["open_times"]
            open_tmp.append(opn)
            restaurants[row]["open_times"] = (
                f"[{opn[0]};{opn[1]};{opn[2]};{opn[3]};{opn[4]};{opn[5]};{opn[6]}]"
                )
            close = restaurants[row]["close_times"]
            close_tmp.append(close)
            restaurants[row]["close_times"] = (
                f"[{close[0]};{close[1]};{close[2]};{close[3]};{close[4]};{close[5]};{close[6]}]"
                )
            restaurants_temp.append(restaurants[row])
        writer.writerows(restaurants_temp)

        j = 0
        for i in restaurants:
            restaurants[i]["open_times"] = open_tmp[j]
            restaurants[i]["close_times"] = close_tmp[j]
            j += 1
