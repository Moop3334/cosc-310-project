from pathlib import Path
import csv
from typing import Dict,Any,List

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "orders.csv"

#TODO: Break down shopping cart into various entries with the same order id, and take all orders with the same order id and convert them to a shopping cart object

def load_all_order() -> List[Dict[str, Any]]:
    if not DATA_PATH.exists():
        raise FileExistsError(
            "Error: The storage csv does not exist or otherwise cannot be accessed"
        )

    orders = []

    with DATA_PATH.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f, delimiter=",")

        for row in reader:
            orders.append(row)
    return orders
    
def load_specific_order(order_id: int) -> Dict[str, Any]:
    orders = load_all_order()
    for order in orders:
        if order["id"] == order_id:
            return order
    raise IndexError(f"Error: Unable to find order id:{order_id}")

def save_all_orders(orders: List[Dict[Any, Any]]) -> None:
    fieldNames = ["id", "user_id", "restaurant_id", "item", "price", "creation_date", "status"]
    with DATA_PATH.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldNames)
        writer.writeheader()
        orders_temp = []
        for row in orders:
            row = dict(row)
            orders_temp.append(row)
        writer.writerows(orders_temp)
        
