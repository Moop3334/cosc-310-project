from pathlib import Path
import csv
from typing import Dict, Any
# pylint: disable=duplicate-code

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "restaurants.csv"

#Returnes a list of dicts where each dict maps to an order
def load_all_restaurants() -> Dict[Any, Dict[Any, Any]]:
    if not DATA_PATH.exists():
        raise FileExistsError(
            "Error: The storage csv does not exist or otherwise cannot be accessed"
            )
    with DATA_PATH.open("r", encoding="utf-8", newline='') as f:
        reader = csv.DictReader(f, delimiter=',')
        orders = {}
        for row in reader:
            row["open_times"] = row["open_times"].strip("[]").split(";")
            row["close_times"] = row["close_times"].strip("[]").split(";")
            orders[row.get("restaurant_id")] = row
        return orders

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
