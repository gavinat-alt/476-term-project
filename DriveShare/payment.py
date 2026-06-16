from database import connect
from session_manager import SessionManager


class RealPayment:

    @staticmethod
    def process_payment(booking_id):

        conn = connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT b.booking_id,
                   b.renter_id,
                   b.total_price,
                   c.owner_id
            FROM bookings b
            JOIN cars c
                ON b.car_id = c.car_id
            WHERE b.booking_id = ?
        """, (booking_id,))

        booking = cursor.fetchone()

        print("DEBUG BOOKING:", booking)

        booking_id, renter_id, amount, owner_id = booking

        print("DEBUG renter_id:", renter_id)
        print("DEBUG owner_id:", owner_id)
        print("DEBUG amount:", amount)

        if booking is None:
            conn.close()
            return False, "Booking not found"

        booking_id, renter_id, amount, owner_id = booking

        cursor.execute(
            "UPDATE users SET balance = balance - ? WHERE user_id = ?",
            (amount, renter_id)
        )

        cursor.execute(
            "UPDATE users SET balance = balance + ? WHERE user_id = ?",
            (amount, owner_id)
        )

        cursor.execute("""
            INSERT INTO payments
            (booking_id, renter_id, owner_id, amount)
            VALUES (?, ?, ?, ?)
        """, (
            booking_id,
            renter_id,
            owner_id,
            amount
        ))

        conn.commit()
        conn.close()

        return True, f"Payment of ${amount:.2f} processed"


class PaymentProxy:

    @staticmethod
    def process_payment(booking_id):

        session = SessionManager()

        if not session.is_logged_in():
            return False, "You must be logged in"

        return RealPayment.process_payment(booking_id)