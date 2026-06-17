# DriveShare Database Schema

## Overview

DriveShare is a peer-to-peer car rental platform where users can list vehicles, rent vehicles, maintain watch lists, exchange messages, and process payments.

The database is implemented using SQLite and consists of six primary tables:

* Users
* Cars
* Bookings
* Watch List
* Payments
* Messages

---

# Entity Relationship Summary

## Users

Stores account information, authentication credentials, balances, account roles, and security questions.

| Column        | Type    | Constraints                |
| ------------- | ------- | -------------------------- |
| user_id       | INTEGER | PRIMARY KEY, AUTOINCREMENT |
| email         | TEXT    | UNIQUE, NOT NULL           |
| password_hash | TEXT    | NOT NULL                   |
| balance       | REAL    | DEFAULT 0                  |
| is_owner      | INTEGER | DEFAULT 0                  |
| is_renter     | INTEGER | DEFAULT 1                  |
| question1     | TEXT    | NOT NULL                   |
| answer1       | TEXT    | NOT NULL                   |
| question2     | TEXT    | NOT NULL                   |
| answer2       | TEXT    | NOT NULL                   |
| question3     | TEXT    | NOT NULL                   |
| answer3       | TEXT    | NOT NULL                   |

### Create Statement

```sql
CREATE TABLE users (
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
);
```

---

## Cars

Stores vehicle listings available for rental.

| Column    | Type    | Constraints                |
| --------- | ------- | -------------------------- |
| car_id    | INTEGER | PRIMARY KEY, AUTOINCREMENT |
| owner_id  | INTEGER | NOT NULL                   |
| model     | TEXT    | NOT NULL                   |
| year      | INTEGER | NOT NULL                   |
| mileage   | INTEGER |                            |
| location  | TEXT    | NOT NULL                   |
| price     | REAL    | NOT NULL                   |
| available | INTEGER | DEFAULT 1                  |

### Create Statement

```sql
CREATE TABLE cars (
    car_id INTEGER PRIMARY KEY AUTOINCREMENT,
    owner_id INTEGER NOT NULL,
    model TEXT NOT NULL,
    year INTEGER NOT NULL,
    mileage INTEGER,
    location TEXT NOT NULL,
    price REAL NOT NULL,
    available INTEGER DEFAULT 1
);
```

---

## Bookings

Records rental transactions between renters and vehicle owners.

| Column      | Type    | Constraints                |
| ----------- | ------- | -------------------------- |
| booking_id  | INTEGER | PRIMARY KEY, AUTOINCREMENT |
| car_id      | INTEGER | NOT NULL                   |
| renter_id   | INTEGER | NOT NULL                   |
| start_date  | TEXT    | NOT NULL                   |
| end_date    | TEXT    | NOT NULL                   |
| total_price | REAL    | NOT NULL                   |

### Create Statement

```sql
CREATE TABLE bookings (
    booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
    car_id INTEGER NOT NULL,
    renter_id INTEGER NOT NULL,
    start_date TEXT NOT NULL,
    end_date TEXT NOT NULL,
    total_price REAL NOT NULL
);
```

---

## Watch List

Allows users to monitor vehicle listings and optionally specify a desired target price.

| Column       | Type    | Constraints                |
| ------------ | ------- | -------------------------- |
| watch_id     | INTEGER | PRIMARY KEY, AUTOINCREMENT |
| user_id      | INTEGER | NOT NULL                   |
| car_id       | INTEGER | NOT NULL                   |
| target_price | REAL    |                            |

### Create Statement

```sql
CREATE TABLE watch_list (
    watch_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    car_id INTEGER NOT NULL,
    target_price REAL
);
```

---

## Payments

Stores completed payment transactions associated with bookings.

| Column       | Type    | Constraints                |
| ------------ | ------- | -------------------------- |
| payment_id   | INTEGER | PRIMARY KEY, AUTOINCREMENT |
| booking_id   | INTEGER | NOT NULL                   |
| renter_id    | INTEGER | NOT NULL                   |
| owner_id     | INTEGER | NOT NULL                   |
| amount       | REAL    | NOT NULL                   |
| payment_date | TEXT    | DEFAULT CURRENT_TIMESTAMP  |

### Create Statement

```sql
CREATE TABLE payments (
    payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    booking_id INTEGER NOT NULL,
    renter_id INTEGER NOT NULL,
    owner_id INTEGER NOT NULL,
    amount REAL NOT NULL,
    payment_date TEXT DEFAULT CURRENT_TIMESTAMP
);
```

---

## Messages

Supports communication between renters and vehicle owners.

| Column       | Type    | Constraints                |
| ------------ | ------- | -------------------------- |
| message_id   | INTEGER | PRIMARY KEY, AUTOINCREMENT |
| sender_id    | INTEGER | NOT NULL                   |
| receiver_id  | INTEGER | NOT NULL                   |
| message_text | TEXT    | NOT NULL                   |
| sent_date    | TEXT    | DEFAULT CURRENT_TIMESTAMP  |

### Create Statement

```sql
CREATE TABLE messages (
    message_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender_id INTEGER NOT NULL,
    receiver_id INTEGER NOT NULL,
    message_text TEXT NOT NULL,
    sent_date TEXT DEFAULT CURRENT_TIMESTAMP
);
```

---

# Sample Seed Data

## Users

```sql
INSERT OR IGNORE INTO users
(email, password_hash, balance, is_owner, is_renter,
 question1, answer1, question2, answer2, question3, answer3)
VALUES
(
    'owner@test.com',
    SHA256('password123'),
    100.0,
    1,
    1,
    'Pet name?', 'fluffy',
    'Favorite color?', 'blue',
    'Birth city?', 'detroit'
);
```

---

# Relationships

### User → Cars

One user may own multiple vehicles.

```
Users (1) -------- (M) Cars
```

### User → Bookings

One user may create multiple bookings.

```
Users (1) -------- (M) Bookings
```

### Car → Bookings

One vehicle may have multiple bookings over time.

```
Cars (1) -------- (M) Bookings
```

### User → Watch List

One user may watch many vehicles.

```
Users (1) -------- (M) Watch_List
```

### Car → Watch List

One vehicle may appear in many watch lists.

```
Cars (1) -------- (M) Watch_List
```

### Booking → Payments

A booking may generate one or more payments.

```
Bookings (1) -------- (M) Payments
```

### Users → Messages

Users may send and receive many messages.

```
Users (1) -------- (M) Messages
```

---

# Database Initialization

The database is initialized using:

```python
create_tables()
create_game_tables()
seed_sample_data()
```

These functions create the schema and populate initial sample data for testing.

---

# Technologies

* Python
* SQLite3
* SHA-256 Password Hashing
* Object-Oriented Design Principles

---

# Notes

* Passwords are never stored in plain text.
* Passwords are hashed using SHA-256 before storage.
* Security questions support password recovery.
* Users may act as both renters and owners.
* Vehicles can be marked available or unavailable.
* Messages include automatic timestamps.
* Payments are associated with bookings and users.
