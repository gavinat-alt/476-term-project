# --- imports ---
import sqlite3
import tkinter as tk
from tkinter import messagebox
import hashlib


# --- helper functions ---
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


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


# --- database connection ---
def connect():
    return sqlite3.connect("driveshare.db")


# --- database table creation ---
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


# --- sample data ---
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


# --- user lookup function ---
def find_user_data_by_email(email):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user_data = cursor.fetchone()

    conn.close()
    return user_data


# --- user registration database function ---
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


# --- singleton pattern: session manager ---
class SessionManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SessionManager, cls).__new__(cls)
            cls._instance.current_user = None
        return cls._instance
    
    def login(self, user):
        self.current_user = user
    
    def logout(self):
        self.current_user = None
        
    def get_current_user(self):
        return self.current_user
    
    def is_logged_in(self):
        return self.current_user is not None


# --- login logic ---
def login_user(email, password):
    email = email.strip().lower()
    user_data = find_user_data_by_email(email)

    if user_data is None:
        return False

    stored_password_hash = user_data[2]

    if hash_password(password) == stored_password_hash:
        user = User(
            userID=user_data[0],
            email=user_data[1],
            password_hash=user_data[2],
            balance=user_data[3]
        )

        session = SessionManager()
        session.login(user)

        return True

    return False


# --- chain of responsibility pattern: security question handler ---
class SecurityQuestionHandler:
    def __init__(self, correct_answer):
        self.correct_answer = correct_answer.lower().strip()
        self.next_handler = None
    
    def set_next(self, handler):
        self.next_handler = handler
        return handler
        
    def check(self, answer, remaining_answers):
        if answer.lower().strip() != self.correct_answer:
            return False

        if self.next_handler is not None:
            if len(remaining_answers) == 0:
                return False

            return self.next_handler.check(
                remaining_answers[0],
                remaining_answers[1:]
            )

        return True


# --- password recovery chain creation ---
def build_recovery_chain(user_data):
    q1_handler = SecurityQuestionHandler(user_data[7])
    q2_handler = SecurityQuestionHandler(user_data[9])
    q3_handler = SecurityQuestionHandler(user_data[11])

    q1_handler.set_next(q2_handler).set_next(q3_handler)

    return q1_handler


# --- password reset logic ---
def reset_password(email, new_password):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE users SET password_hash = ? WHERE email = ?",
        (hash_password(new_password), email.strip().lower())
    )

    conn.commit()
    conn.close()


def recover_password(email, answer1, answer2, answer3, new_password):
    email = email.strip().lower()
    user_data = find_user_data_by_email(email)

    if user_data is None:
        return False, "Email not found"

    recovery_chain = build_recovery_chain(user_data)

    if recovery_chain.check(answer1, [answer2, answer3]):
        reset_password(email, new_password)
        return True, "Password reset successful"
    else:
        return False, "Incorrect answers to security questions"


# --- tkinter setup ---
root = tk.Tk()
root.title("DriveShare")
root.geometry("450x650")


# --- tkinter helper ---
def clear_window():
    for widget in root.winfo_children():
        widget.destroy()


# --- login screen ---
def show_login_screen():
    clear_window()

    tk.Label(root, text="DriveShare Login", font=("Arial", 18)).pack(pady=10)

    tk.Label(root, text="Email:").pack()
    email_entry = tk.Entry(root)
    email_entry.pack()

    tk.Label(root, text="Password:").pack()
    password_entry = tk.Entry(root, show="*")
    password_entry.pack()

    def login_button_clicked():
        email = email_entry.get()
        password = password_entry.get()

        if email.strip() == "" or password.strip() == "":
            messagebox.showerror("Error", "Email and password are required")
            return
        
        if login_user(email, password):
            messagebox.showinfo("Success", "Login successful")
            show_logged_in_screen()
        else:
            messagebox.showerror("Error", "Invalid email or password")

    tk.Button(root, text="Login", command=login_button_clicked).pack(pady=5)
    tk.Button(root, text="Create Account", command=show_register_screen).pack(pady=5)
    tk.Button(root, text="Forgot Password", command=show_recovery_screen).pack(pady=5)


# --- register screen ---
def show_register_screen():
    clear_window()

    tk.Label(root, text="Create Account", font=("Arial", 18)).pack(pady=10)

    tk.Label(root, text="Email:").pack()
    email_entry = tk.Entry(root)
    email_entry.pack()

    tk.Label(root, text="Password:").pack()
    password_entry = tk.Entry(root, show="*")
    password_entry.pack()

    tk.Label(root, text="Security Question 1:").pack()
    q1_entry = tk.Entry(root)
    q1_entry.pack()

    tk.Label(root, text="Answer 1:").pack()
    a1_entry = tk.Entry(root)
    a1_entry.pack()

    tk.Label(root, text="Security Question 2:").pack()
    q2_entry = tk.Entry(root)
    q2_entry.pack()

    tk.Label(root, text="Answer 2:").pack()
    a2_entry = tk.Entry(root)
    a2_entry.pack()

    tk.Label(root, text="Security Question 3:").pack()
    q3_entry = tk.Entry(root)
    q3_entry.pack()

    tk.Label(root, text="Answer 3:").pack()
    a3_entry = tk.Entry(root)
    a3_entry.pack()

    def submit_register():
        email = email_entry.get()
        password = password_entry.get()
        q1 = q1_entry.get()
        a1 = a1_entry.get()
        q2 = q2_entry.get()
        a2 = a2_entry.get()
        q3 = q3_entry.get()
        a3 = a3_entry.get()

        fields = [email, password, q1, a1, q2, a2, q3, a3]

        if any(field.strip() == "" for field in fields):
            messagebox.showerror("Error", "All fields are required")
            return

        success, message = register_user(email, password, q1, a1, q2, a2, q3, a3)

        if success:
            messagebox.showinfo("Success", message)
            show_login_screen()
        else:
            messagebox.showerror("Error", message)

    tk.Button(root, text="Create Account", command=submit_register).pack(pady=5)
    tk.Button(root, text="Back to Login", command=show_login_screen).pack(pady=5)


# --- password recovery screen ---
def show_recovery_screen():
    clear_window()

    tk.Label(root, text="Password Recovery", font=("Arial", 18)).pack(pady=10)

    tk.Label(root, text="Email:").pack()
    email_entry = tk.Entry(root)
    email_entry.pack()

    question1_label = tk.Label(root, text="Question 1")
    question1_label.pack()
    answer1_entry = tk.Entry(root)
    answer1_entry.pack()

    question2_label = tk.Label(root, text="Question 2")
    question2_label.pack()
    answer2_entry = tk.Entry(root)
    answer2_entry.pack()

    question3_label = tk.Label(root, text="Question 3")
    question3_label.pack()
    answer3_entry = tk.Entry(root)
    answer3_entry.pack()

    tk.Label(root, text="New Password:").pack()
    new_password_entry = tk.Entry(root, show="*")
    new_password_entry.pack()

    def load_questions():
        email = email_entry.get().strip().lower()

        if email == "":
            messagebox.showerror("Error", "Enter your email first")
            return

        user_data = find_user_data_by_email(email)

        if user_data is None:
            messagebox.showerror("Error", "Email not found")
            return

        question1_label.config(text=user_data[6])
        question2_label.config(text=user_data[8])
        question3_label.config(text=user_data[10])

    def submit_recovery():
        email = email_entry.get()
        answer1 = answer1_entry.get()
        answer2 = answer2_entry.get()
        answer3 = answer3_entry.get()
        new_password = new_password_entry.get()

        fields = [email, answer1, answer2, answer3, new_password]

        if any(field.strip() == "" for field in fields):
            messagebox.showerror("Error", "All fields are required")
            return

        success, message = recover_password(
            email,
            answer1,
            answer2,
            answer3,
            new_password
        )

        if success:
            messagebox.showinfo("Success", message)
            show_login_screen()
        else:
            messagebox.showerror("Error", message)

    tk.Button(root, text="Load Security Questions", command=load_questions).pack(pady=5)
    tk.Button(root, text="Reset Password", command=submit_recovery).pack(pady=5)
    tk.Button(root, text="Back to Login", command=show_login_screen).pack(pady=5)


# --- logged in screen ---
def show_logged_in_screen():
    clear_window()

    session = SessionManager()
    current_user = session.get_current_user()

    if current_user is None:
        show_login_screen()
        return

    tk.Label(root, text="Welcome to DriveShare", font=("Arial", 18)).pack(pady=10)
    tk.Label(root, text=f"Logged in as: {current_user.email}").pack()
    tk.Label(root, text=f"Balance: ${current_user.balance:.2f}").pack()

    def logout_clicked():
        session.logout()
        messagebox.showinfo("Logged Out", "You have been logged out")
        show_login_screen()

    tk.Button(root, text="Logout", command=logout_clicked).pack(pady=10)


# --- program startup ---
create_tables()
seed_sample_data()

session = SessionManager()

show_login_screen()

root.mainloop()