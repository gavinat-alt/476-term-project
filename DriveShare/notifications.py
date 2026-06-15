from database import connect

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