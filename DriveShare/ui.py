# --- tkinter UI ---

import tkinter as tk
from tkinter import messagebox

from car_booking import CarService, BookingService, WatchObserver
from database import register_user, find_user_data_by_email
from auth import login_user
from password_recovery import recover_password
from session_manager import SessionManager
from payment import PaymentProxy
from messaging import MessageService
from mediator import UIMediator


ui_mediator = UIMediator()


def clear_window(root):
    for widget in root.winfo_children():
        widget.destroy()


def show_login_screen(root):
    clear_window(root)

    ui_mediator.register(
        "login_screen",
        lambda: show_login_screen(root)
    )

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
            show_logged_in_screen(root)
        else:
            messagebox.showerror("Error", "Invalid email or password")

    tk.Button(root, text="Login", command=login_button_clicked).pack(pady=5)
    tk.Button(root, text="Create Account", command=lambda: show_register_screen(root)).pack(pady=5)
    tk.Button(root, text="Forgot Password", command=lambda: show_recovery_screen(root)).pack(pady=5)


def show_register_screen(root):
    clear_window(root)

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
            show_login_screen(root)
        else:
            messagebox.showerror("Error", message)

    tk.Button(root, text="Create Account", command=submit_register).pack(pady=5)
    tk.Button(root, text="Back to Login", command=lambda: show_login_screen(root)).pack(pady=5)


def show_recovery_screen(root):
    clear_window(root)

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
            show_login_screen(root)
        else:
            messagebox.showerror("Error", message)

    tk.Button(root, text="Load Security Questions", command=load_questions).pack(pady=5)
    tk.Button(root, text="Reset Password", command=submit_recovery).pack(pady=5)
    tk.Button(root, text="Back to Login", command=lambda: show_login_screen(root)).pack(pady=5)


def show_logged_in_screen(root):
    clear_window(root)

    session = SessionManager()
    current_user = session.get_current_user()

    if current_user is None:
        show_login_screen(root)
        return

    tk.Label(root, text="Welcome to DriveShare", font=("Arial", 18)).pack(pady=10)
    tk.Label(root, text=f"User ID: {current_user.userID}").pack()
    tk.Label(root, text=f"Logged in as: {current_user.email}").pack()

    from database import get_user_balance

    balance_label = tk.Label(root)
    balance_label.pack()

    def refresh_balance():
        balance = get_user_balance(current_user.userID)
        balance_label.config(text=f"Balance: ${balance:.2f}")

    refresh_balance()

    tk.Button(
        root,
        text="View Cars",
        command=lambda: show_cars_screen(root)
    ).pack(pady=5)

    tk.Button(
        root,
        text="Add Car",
        command=lambda: show_add_car_screen(root)
    ).pack(pady=5)

    tk.Button(
        root,
        text="Book Car",
        command=lambda: show_booking_screen(root)
    ).pack(pady=5)

    tk.Button(
        root,
        text="Make Payment",
        command=lambda: show_payment_screen(root)
    ).pack(pady=5)

    tk.Button(
        root,
        text="Send Message",
        command=lambda: show_send_message_screen(root)
    ).pack(pady=5)

    tk.Button(
        root,
        text="View Messages",
        command=lambda: show_messages_screen(root)
    ).pack(pady=5)

    tk.Button(
        root,
        text="Rental History",
        command=lambda: show_history_screen(root)
    ).pack(pady=5)

    def logout_clicked():
        session.logout()
        messagebox.showinfo("Logged Out", "You have been logged out")
        show_login_screen(root)

    tk.Button(root, text="Logout", command=logout_clicked).pack(pady=10)

def show_add_car_screen(root):
    win = tk.Toplevel(root)
    win.title("Add Car")

    tk.Label(win, text="Car Model (e.g. Ford):").pack()
    model = tk.Entry(win)
    model.pack()

    tk.Label(win, text="Year:").pack()
    year = tk.Entry(win)
    year.pack()

    tk.Label(win, text="Mileage:").pack()
    mileage = tk.Entry(win)
    mileage.pack()

    tk.Label(win, text="Location:").pack()
    location = tk.Entry(win)
    location.pack()

    tk.Label(win, text="Price:").pack()
    price = tk.Entry(win)
    price.pack()

    def submit():
        model_val = model.get().strip()
        year_val = year.get().strip()
        mileage_val = mileage.get().strip()
        location_val = location.get().strip()
        price_val = price.get().strip()

        if not model_val or not year_val or not mileage_val or not location_val or not price_val:
            messagebox.showerror("Error", "All fields are required")
            return

        try:
            year_val = int(year_val)
            mileage_val = int(mileage_val)
            price_val = float(price_val)
        except ValueError:
            messagebox.showerror("Error", "Year, mileage, and price must be numbers")
            return

        success, msg = CarService.add_car(
            model_val,
            year_val,
            mileage_val,
            location_val,
            price_val
        )

        messagebox.showinfo("Result", msg)
        win.destroy()

    tk.Button(win, text="Add", command=submit).pack()

def show_cars_screen(root):
    win = tk.Toplevel(root)
    win.title("Cars")

    from car_booking import CarService
    cars = CarService.get_all_cars()

    for c in cars:
        tk.Label(win, text=str(c)).pack()

def show_booking_screen(root):
    win = tk.Toplevel(root)
    win.title("Book Car")

    tk.Label(win, text="Car ID (number from car list):").pack()
    car_id = tk.Entry(win)
    car_id.pack()

    tk.Label(win, text="Start Date (YYYY-MM-DD):").pack()
    start = tk.Entry(win)
    start.pack()

    tk.Label(win, text="End Date (YYYY-MM-DD):").pack()
    end = tk.Entry(win)
    end.pack()

    def submit():

        try:
            car_num = int(car_id.get())
        except ValueError:
            messagebox.showerror(
                "Error",
                "Car ID must be a number"
            )
            return

        success, msg = BookingService.book_car(
            car_num,
            start.get(),
            end.get()
        )

        if success:
            messagebox.showinfo(
                "Booking Status",
                msg
            )
        else:
            messagebox.showerror(
                "Booking Status",
                msg
            )

    tk.Button(win, text="Book", command=submit).pack()

def show_payment_screen(root):

    win = tk.Toplevel(root)
    win.title("Payment")

    tk.Label(
        win,
        text="Booking ID:"
    ).pack()

    booking_id = tk.Entry(win)
    booking_id.pack()

    def submit():

        try:
            booking_num = int(
                booking_id.get()
            )
        except ValueError:
            messagebox.showerror(
                "Error",
                "Booking ID must be a number"
            )
            return

        success, msg = PaymentProxy.process_payment(booking_num)

        if success:
            messagebox.showinfo("Payment", msg)
            show_logged_in_screen(root)  # <-- ADD THIS
        else:
            messagebox.showerror("Payment", msg)

    tk.Button(
        win,
        text="Pay"
    ,
        command=submit
    ).pack(pady=10)

def show_send_message_screen(root):

    win = tk.Toplevel(root)
    win.title("Send Message")

    tk.Label(
        win,
        text="Receiver User ID:"
    ).pack()

    receiver = tk.Entry(win)
    receiver.pack()

    tk.Label(
        win,
        text="Message:"
    ).pack()

    message_box = tk.Entry(win, width=40)
    message_box.pack()

    def submit():

        try:
            receiver_id = int(receiver.get())
        except ValueError:
            messagebox.showerror(
                "Error",
                "Receiver ID must be a number"
            )
            return

        success, msg = MessageService.send_message(
            receiver_id,
            message_box.get()
        )

        if success:
            messagebox.showinfo(
                "Message",
                msg
            )
            win.destroy()
        else:
            messagebox.showerror(
                "Message",
                msg
            )

    tk.Button(
        win,
        text="Send",
        command=submit
    ).pack(pady=10)

def show_messages_screen(root):

    win = tk.Toplevel(root)
    win.title("My Messages")

    messages = MessageService.get_my_messages()

    if not messages:
        tk.Label(
            win,
            text="No messages"
        ).pack()
        return

    for msg in messages:

        tk.Label(
            win,
            text=f"From User {msg[0]}: {msg[1]}"
        ).pack()

def show_history_screen(root):
    win = tk.Toplevel(root)
    win.title("Rental History")

    session = SessionManager()
    user = session.get_current_user()

    from car_booking import BookingService
    history = BookingService.get_user_history(user.userID)

    if not history:
        tk.Label(win, text="No rentals found").pack()
        return

    for h in history:
        tk.Label(
            win,
            text=f"Booking #{h[0]} | Car {h[1]} | {h[2]} → {h[3]} | ${h[4]}"
        ).pack()