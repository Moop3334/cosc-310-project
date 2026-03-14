class DeliveryDriver():
    def __init__(self, driver_id, name, phone_number):
        self.driver_id = driver_id
        self.name = name
        self.phone_number = phone_number
        self.completed_orders = []

    def get_id(self):
        return self.driver_id

    def get_name(self):
        return self.name

    def get_phone_number(self):
        return self.phone_number

    def complete_order(self, order):
        if order is None:
            return False
        self.completed_orders.append(order)
        return True
    