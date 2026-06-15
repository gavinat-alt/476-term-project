from database import connect
from session_manager import SessionManager
from datetime import datetime

class CarService:

    @staticmethod
    def add_car(model, year, mileage, location, price):
        session = SessionManager()
        user = session.get_current_user()

        if not user:
            return False, "Not logged in"

        conn = connect()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO cars (owner_id, model, year, mileage, location, price)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user.userID, model, year, mileage, location, price))

        conn.commit()
        conn.close()

        return True, "Car added successfully"

    @staticmethod
    def get_all_cars():
        conn = connect()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM cars")
        cars = cursor.fetchall()

        conn.close()
        return cars

class BookingService:

    @staticmethod
    def is_available(car_id, start_date, end_date):
        conn = connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM bookings
            WHERE car_id = ?
            AND (
                (start_date <= ? AND end_date >= ?) OR
                (start_date <= ? AND end_date >= ?) OR
                (start_date >= ? AND end_date <= ?)
            )
        """, (car_id, end_date, end_date, start_date, start_date, start_date, end_date))

        conflict = cursor.fetchone()
        conn.close()

        return conflict is None

    @staticmethod
    def book_car(car_id, start_date, end_date):
        session = SessionManager()
        user = session.get_current_user()

        if not user:
            return False, "Not logged in"

        if not BookingService.is_available(car_id, start_date, end_date):
            return False, "Car already booked for these dates"

        conn = connect()
        cursor = conn.cursor()

        # simple price calc (placeholder)
        cursor.execute("SELECT price FROM cars WHERE car_id = ?", (car_id,))
        price = cursor.fetchone()[0]

        total_price = price

        cursor.execute("""
            INSERT INTO bookings (car_id, renter_id, start_date, end_date, total_price)
            VALUES (?, ?, ?, ?, ?)
        """, (car_id, user.userID, start_date, end_date, total_price))

        conn.commit()
        conn.close()

        return True, "Booking successful"

class WatchObserver:

    @staticmethod
    def watch_car(car_id, target_price):
        session = SessionManager()
        user = session.get_current_user()

        conn = connect()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO watch_list (user_id, car_id, target_price)
            VALUES (?, ?, ?)
        """, (user.userID, car_id, target_price))

        conn.commit()
        conn.close()

        return True, "Car added to watch list"