class DeliveryDriver:
    def __init__(self, driver_id, name, phone_number, username, email, password_hash, vehicle_type=None, is_active=True):
        self.driver_id = driver_id
        self.name = name.strip()
        self.phone_number = phone_number.strip()
        self.username = username.strip()
        self.email = email.strip().lower()
        self.password_hash = password_hash
        self.vehicle_type = vehicle_type
        self.is_active = is_active
        self.completed_orders = []

    def get_id(self):
        return self.driver_id

    def get_name(self):
        return self.name

    def get_phone_number(self):
        return self.phone_number

    def get_username(self):
        return self.username

    def get_email(self):
        return self.email

    def get_vehicle_type(self):
        return self.vehicle_type

    def get_is_active(self):
        return self.is_active

    def can_login(self):
        return self.is_active and self.username != "" and self.password_hash != ""

    def complete_order(self, order_id):
        if not self.is_active:
            return False
        if order_id is None:
            return False
        if order_id in self.completed_orders:
            return False

        self.completed_orders.append(order_id)
        return True

    def deactivate(self):
        self.is_active = False

    def activate(self):
        self.is_active = True