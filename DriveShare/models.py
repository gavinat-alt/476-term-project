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
        

class Booking:
    def __init__(self, car_id, renter_id, start_date, end_date):
        self.car_id = car_id
        self.renter_id = renter_id
        self.start_date = start_date
        self.end_date = end_date