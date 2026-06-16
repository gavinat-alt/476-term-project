# --- model classes ---

class User:
    def __init__(self, userID, email, password_hash, balance=0.0):
        self.userID = userID
        self.email = email
        self.password = password_hash
        self.balance = balance
        self.is_owner = False
        self.is_renter = True
        
    def become_owner(self):
        self.is_owner = True
        
    def add_balance(self, amount):
        self.balance += amount
        
    def subtract_balance(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            return True
        return False
    

class Car:
    def __init__(self, car_id, owner_id, model, year, location, price):
        self.car_id = car_id
        self.owner_id = owner_id
        self.model = model
        self.year = year
        self.location = location
        self.price = price

class CarBuilder:

    def __init__(self):
        self.car_data = {}

    def set_owner_id(self, owner_id):
        self.car_data["owner_id"] = owner_id
        return self

    def set_model(self, model):
        self.car_data["model"] = model
        return self

    def set_year(self, year):
        self.car_data["year"] = year
        return self

    def set_mileage(self, mileage):
        self.car_data["mileage"] = mileage
        return self

    def set_location(self, location):
        self.car_data["location"] = location
        return self

    def set_price(self, price):
        self.car_data["price"] = price
        return self

    def build(self):
        return self.car_data
        

class Booking:
    def __init__(self, car_id, renter_id, start_date, end_date):
        self.car_id = car_id
        self.renter_id = renter_id
        self.start_date = start_date
        self.end_date = end_date