# --- database functions ---

import sqlite3
import hashlib


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def connect():
    return sqlite3.connect("driveshare.db")


def create_tables():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            balance REAL DEFAULT 0,
            is_owner INTEGER DEFAULT 0,
            is_renter INTEGER DEFAULT 1,
            question1 TEXT NOT NULL,
            answer1 TEXT NOT NULL,
            question2 TEXT NOT NULL,
            answer2 TEXT NOT NULL,
            question3 TEXT NOT NULL,
            answer3 TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def seed_sample_data():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO users 
        (email, password_hash, balance, is_owner, is_renter,
         question1, answer1, question2, answer2, question3, answer3)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        "owner@test.com",
        hash_password("password123"),
        100.0,
        1,
        1,
        "Pet name?", "fluffy",
        "Favorite color?", "blue",
        "Birth city?", "detroit"
    ))

    conn.commit()
    conn.close()


def find_user_data_by_email(email):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user_data = cursor.fetchone()

    conn.close()
    return user_data


def register_user(email, password, q1, a1, q2, a2, q3, a3):
    email = email.strip().lower()

    if find_user_data_by_email(email) is not None:
        return False, "Email already registered"

    conn = connect()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO users 
            (email, password_hash, question1, answer1, question2, answer2, question3, answer3)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            email,
            hash_password(password),
            q1.strip(),
            a1.strip(),
            q2.strip(),
            a2.strip(),
            q3.strip(),
            a3.strip()
        ))

        conn.commit()
        return True, "Account created successfully"

    except sqlite3.IntegrityError:
        return False, "Email already registered"

    finally:
        conn.close()


def reset_password(email, new_password):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE users SET password_hash = ? WHERE email = ?",
        (hash_password(new_password), email.strip().lower())
    )

    conn.commit()
    conn.close()


def create_game_tables():
    conn = connect()
    cursor = conn.cursor()

    # CAR LISTINGS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cars (
            car_id INTEGER PRIMARY KEY AUTOINCREMENT,
            owner_id INTEGER NOT NULL,
            model TEXT NOT NULL,
            year INTEGER NOT NULL,
            mileage INTEGER,
            location TEXT NOT NULL,
            price REAL NOT NULL,
            available INTEGER DEFAULT 1
        )
    """)

    # BOOKINGS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
            car_id INTEGER NOT NULL,
            renter_id INTEGER NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            total_price REAL NOT NULL
        )
    """)

    # OBSERVER (WATCH LIST)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS watch_list (
            watch_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            car_id INTEGER NOT NULL,
            target_price REAL
        )
    """)


    # PAYMENTS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS payments (
            payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            booking_id INTEGER NOT NULL,
            renter_id INTEGER NOT NULL,
            owner_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            payment_date TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)


    # MESSAGES
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            message_id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender_id INTEGER NOT NULL,
            receiver_id INTEGER NOT NULL,
            message_text TEXT NOT NULL,
            sent_date TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS payments
                   (
                       payment_id
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       booking_id
                       INTEGER,
                       renter_id
                       INTEGER,
                       owner_id
                       INTEGER,
                       amount
                       REAL
                   )
                   """)


    conn.commit()
    conn.close()

def get_user_balance(user_id):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()

    conn.close()
    return result[0] if result else 0

def fix_car_ownership():
    conn = connect()
    cursor = conn.cursor()

    # change ALL cars owned by user 5 → user 1 (example)
    cursor.execute("""
        UPDATE cars
        SET owner_id = 1
        WHERE owner_id = 5
    """)

    conn.commit()
    conn.close()

    print("Car ownership fixed")