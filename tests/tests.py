# auth_utils.py

import bcrypt

class User:    
    def __init__(self, username, password):
        self.username = username
        self.password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    def check_password(self, password):
        return bcrypt.checkpw(password.encode(), self.password.encode())

def register_user(username, password):
    return f"User {username} registered successfully."

def login(username, password):
    return f"User {username} logged in successfully. Here's your token."

def reset_password(username, new_password):
    return f"Password for user {username} reset successfully."
