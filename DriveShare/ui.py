# --- tkinter UI ---

import tkinter as tk
from tkinter import messagebox

from database import register_user, find_user_data_by_email
from auth import login_user
from password_recovery import recover_password
from session_manager import SessionManager


def clear_window(root):
    for widget in root.winfo_children():
        widget.destroy()


def show_login_screen(root):
    clear_window(root)

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
    tk.Label(root, text=f"Logged in as: {current_user.email}").pack()
    tk.Label(root, text=f"Balance: ${current_user.balance:.2f}").pack()

    def logout_clicked():
        session.logout()
        messagebox.showinfo("Logged Out", "You have been logged out")
        show_login_screen(root)

    tk.Button(root, text="Logout", command=logout_clicked).pack(pady=10)