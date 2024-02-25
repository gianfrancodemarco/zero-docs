# auth_utils.py

"""A module for user authentication utilities.

This module provides functionalities for user authentication, including user registration, login, password management, and user class with encrypted password storage.

Classes:
    User: A class representing a user in the system.

Methods:
    register_user: Register a new user with a username and password.
    login: Simulate a user login process and generate a login token.
    reset_password: Reset the password for a given user.
    
Exceptions:
    No exceptions are explicitly defined in this module.

Additional Notes:
    - The User class utilizes bcrypt to securely hash and store passwords.
    - Each function provides clear docstrings to explain inputs, outputs, and functionality.
"""
import bcrypt

class User:
    """A class representing a user in the system. 
    
    Attributes:
        username (str): The username of the user.
        password (str): The hashed password of the user.
    
    Methods:
        __init__: Initializes a User object with a username and a password hashed using bcrypt.
        check_password: Checks if the provided password matches the stored password after encoding using bcrypt.
    """
    def __init__(self, username, password):
        """Initialize a User object with a username and password hashed using bcrypt.
        
        Args:
            username (str): The username of the user.
            password (str): The password of the user.
        
        Returns:
            None
        """
        self.username = username
        self.password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    def check_password(self, password):
        """Check if the provided password matches the stored password after encoding using bcrypt.
        
        Args:
            password (str): The password to be checked.
        
        Returns:
            bool: True if the provided password matches the stored password, False otherwise.
        """
        return bcrypt.checkpw(password.encode(), self.password.encode())

def register_user(username, password):
    """
    Register a new user with the provided username and password.
    
    Parameters:
    - username (str): The username of the user being registered.
    - password (str): The password associated with the user.
    
    Returns:
    str: A message confirming successful user registration.
    
    """
    return f"User {username} registered successfully."

def login(username, password):
    """Simulate a user login process and generate a login token.
    
    Args:
        username (str): The username of the user attempting to log in.
        password (str): The password provided by the user for authentication.
    
    Returns:
        str: A success message along with a login token if the user login is successful.
    """
    return f"User {username} logged in successfully. Here's your token."

def reset_password(username, new_password):
    """
    Reset the password for a given user.
    
    Args:
        username (str): The username of the user for whom the password is being reset.
        new_password (str): The new password to set for the user.
    
    Returns:
        str: A message indicating that the password reset was successful.
    """
    return f"Password for user {username} reset successfully."
