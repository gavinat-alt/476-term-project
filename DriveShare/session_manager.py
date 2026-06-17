# --- singleton pattern: session manager ---

class SessionManager:
    _instance = None

    def __new__(cls): # ensure only one instance of SessionManager exists
        if cls._instance is None:
            cls._instance = super(SessionManager, cls).__new__(cls)
            cls._instance.current_user = None
        return cls._instance
    
    def login(self, user): # set the current user when they log in
        self.current_user = user
    
    def logout(self): # clear the current user when they log out
        self.current_user = None
        
    def get_current_user(self): # return the current logged-in user, or None if no user is logged in
        return self.current_user
    
    def is_logged_in(self): # return True if a user is currently logged in, False otherwise
        return self.current_user is not None