from pathlib import Path
import csv
from typing import Dict, Any, List
import json

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "orders.csv"

#TODO: Break down shopping cart into various entries with the same order id, and take all orders with the same order id and convert them to a shopping cart object

def load_all_order() -> List[Dict[str, Any]]:
    """Load all orders from CSV, parsing items JSON."""
    if not DATA_PATH.exists():
        raise FileExistsError(
            "Error: The storage csv does not exist or otherwise cannot be accessed"
        )
    orders = []
    with DATA_PATH.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f, delimiter=",")
        for row in reader:
            # Parse items JSON if present
            if "items" in row and row["items"]:
                try:
                    row["items"] = json.loads(row["items"])
                except json.JSONDecodeError:
                    row["items"] = []
            else:
                row["items"] = []
            
            # Convert total_price to float
            if "total_price" in row:
                try:
                    row["total_price"] = float(row["total_price"])
                except (ValueError, TypeError):
                    row["total_price"] = 0.0
            
            orders.append(row)
    return orders
    
def load_specific_order(order_id: int) -> Dict[str, Any]:
    orders = load_all_order()
    for order in orders:
        if order.id == order_id:
            return order
    raise IndexError(f"Error: Unable to find order id:{order_id}")

def save_all_orders(orders: List[Dict[Any, Any]]) -> None:
    fieldNames = ["id", "user_id", "restaurant_id", "items", "total_price", "creation_date", "status"]
    with DATA_PATH.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldNames)
        writer.writeheader()

        for order in orders:
            print(order)
            row = {
                "id": str(order.id),
                "user_id": str(order.user_id),
                "restaurant_id": str(order.restaurant_id),
                "items": json.dumps([item.model_dump() for item in order.items]),
                "total_price": str(order.total_price),
                "creation_date": str(order.creation_date),
                "status": str(order.status)
            }
            writer.writerow(row)
        
