class User():
    def __init__(self, user_id, name, phone_number, address):
        self.user_id = user_id
        self.name = name
        self.phone_number = phone_number
        self.address = address

    def get_id(self):
        return self.user_id

    def get_name(self):
        return self.name

    def get_phone_number(self):
        return self.phone_number

    def get_address(self):
        return self.address

    def create_order(self, menu_items):
        # TODO: import Order class when Qiran finishes OrderClass branch
        if not menu_items:
            return None
        return None

    def cancel_order(self, order):
        if order is None:
            return False
        if order.status == "delivered":
            return False
        order.status = "cancelled"
        return True
    