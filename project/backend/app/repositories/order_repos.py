from pathlib import Path
import csv
from typing import Dict,Any,List

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "food_delivery.csv"
COLUMNS_TO_KEEP = ["order_id", "customer_id", "restaurant_id", "food_item", "order_time"]

def load_all_order() -> List[Dict[str, Any]]:
    if not DATA_PATH.exists():
        raise FileExistsError(
            "Error: The storage csv does not exist or otherwise cannot be accessed"
        )

    orders: List[Dict[str, Any]] = []

    with DATA_PATH.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f, delimiter=",")

        for row in reader:
            filtered_row = {col: row[col] for col in COLUMNS_TO_KEEP}
            orders.append(filtered_row)
    return orders
    

def save_all_orders(orders: List[Dict[Any, Any]]) -> None:
    fieldNames = ["order_id", "customer_id", "restaurant_id", "food_item", "order_time"]
    with DATA_PATH.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldNames)
        writer.writeheader()
        orders_temp = []
        for row in orders:
            row = dict(row)
            orders_temp.append(row)
        writer.writerows(orders_temp)
        


