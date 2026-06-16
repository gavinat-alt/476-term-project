# --- main program ---

import tkinter as tk

from database import create_tables, seed_sample_data, create_game_tables
from session_manager import SessionManager
from ui import show_login_screen



create_tables()
create_game_tables()
seed_sample_data()

session = SessionManager()

root = tk.Tk()
root.title("DriveShare")
root.geometry("450x650")

show_login_screen(root)

root.mainloop()