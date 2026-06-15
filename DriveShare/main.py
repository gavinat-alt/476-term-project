# --- main program ---

import tkinter as tk

from database import create_tables, seed_sample_data
from session_manager import SessionManager
from ui import show_login_screen


create_tables()
seed_sample_data()

session = SessionManager()

root = tk.Tk()
root.title("DriveShare")
root.geometry("450x650")

show_login_screen(root)

root.mainloop()