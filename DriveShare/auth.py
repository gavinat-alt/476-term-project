# --- login logic ---

from database import find_user_data_by_email, hash_password
from models import User
from session_manager import SessionManager


def login_user(email, password): # return True if login successful, False otherwise
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

        session = SessionManager() # get the singleton session manager instance
        session.login(user) # log the user in by setting the current user in the session manager

        return True

    return False