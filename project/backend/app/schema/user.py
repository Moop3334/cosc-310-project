from order import Order

class User():
    def __init__(self, id, name, phone_number, address):
        self.id = id
        self.name = name
        self.phone_number = phone_number
        self.address = address

    # Getter
    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_phone_number(self):
        return self.phone_number

    def get_address(self):
        return self.address

    # Create order
    def create_order(self, menu_items):
        if not menu_items:
            return None
        order = Order(
            user=self,
            menu_items=menu_items
        )
        return order

    # Cancel order
    def cancel_order(self, order):
        if order is None:
            return False
        if order.status == "delivered":
            return False
        order.status = "cancelled"
        return True