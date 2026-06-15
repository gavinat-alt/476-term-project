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