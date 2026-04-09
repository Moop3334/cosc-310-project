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
        if int(order["id"]) == order_id:
            return order
    raise IndexError(f"Error: Unable to find order id:{order_id}")

def save_all_orders(orders: List[Dict[Any, Any]]) -> None:
    fieldNames = ["id", "user_id", "restaurant_id", "items", "total_price", "creation_date", "status"]
    with DATA_PATH.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldNames)
        writer.writeheader()

        for order in orders:
            # Handle both dict and Order object formats
            items_data = order.get("items", []) if isinstance(order, dict) else order.items
            if items_data and not isinstance(items_data, str):
                try:
                    items_json = json.dumps([item.model_dump() if hasattr(item, 'model_dump') else item for item in items_data])
                except (AttributeError, TypeError):
                    items_json = json.dumps(items_data)
            else:
                items_json = order.get("items", "") if isinstance(order, dict) else ""
            
            row = {
                "id": str(order.get("id") if isinstance(order, dict) else order.id),
                "user_id": str(order.get("user_id") if isinstance(order, dict) else order.user_id),
                "restaurant_id": str(order.get("restaurant_id") if isinstance(order, dict) else order.restaurant_id),
                "items": items_json,
                "total_price": str(order.get("total_price") if isinstance(order, dict) else order.total_price),
                "creation_date": str(order.get("creation_date") if isinstance(order, dict) else order.creation_date),
                "status": str(order.get("status") if isinstance(order, dict) else order.status)
            }
            writer.writerow(row)
        
