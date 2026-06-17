from database import connect
## this function checks if there are any users watching a car that has just been updated with 
# a new price, and if so, prints a notification for each user whose target price is met or exceeded 
# by the new price. This allows users to be notified when a car they are interested in becomes
# available at a price they are willing to pay.
def check_watch_notifications(car_id, new_price):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT user_id, target_price FROM watch_list
        WHERE car_id = ?
    """, (car_id,))

    watchers = cursor.fetchall()

    for user_id, target_price in watchers:
        if target_price is None or new_price <= target_price:
            print(f"NOTIFY USER {user_id}: Car {car_id} is now available at {new_price}")

    conn.close()