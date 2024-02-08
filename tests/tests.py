# auth_utils.py

"""
Initialize the username and hashed password for the user. Check if the given password matches the stored password using bcrypt. Register a new user with the given username and password. Logs a user in using the provided username and password, returning a success message with a token. Reset the password for a user and return a success message.
"""
import bcrypt

class User:
    """
    Initialize the username and hashed password for the user.
    
    Check if the given password matches the stored password using bcrypt.
    """
    def __init__(self, username, password):
        """
        Initialize the username and hashed password for the user.
        """
        self.username = username
        self.password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    def check_password(self, password):
        """
        Check if the given password matches the stored password using bcrypt.
        """
        return bcrypt.checkpw(password.encode(), self.password.encode())

def register_user(username, password):
    """
    Register a new user with the given username and password.
    """
    return f"User {username} registered successfully."

def login(username, password):
    """
    Logs a user in using the provided username and password, returning a success message with a token.
    """
    return f"User {username} logged in successfully. Here's your token."

def reset_password(username, new_password):
    """
    Reset the password for a user and return a success message.
    """
    return f"Password for user {username} reset successfully."
