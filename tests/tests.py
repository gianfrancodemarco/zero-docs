"""A module for user management functionality.

This module includes a User class that represents a user with a username and a hashed password using bcrypt. 
It also provides functions for user registration, login, and password reset.

Classes:
    User: A class representing a user with a username and a hashed password.

Methods:
    - register_user: Register a user with a provided username and password.
    - login: Simulate a user login process.
    - reset_password: Reset the password for a specific user.

Exceptions:
    None
"""
import bcrypt

class User:
    """A user class that represents a user of the application. 
    
    Attributes:
        - username (str): The username of the user.
        - password (str): The hashed password of the user using bcrypt.
    
    Methods:
        - check_password: A method to check if the provided password matches the stored hashed password.
    """
    def __init__(self, username, password):
        """Initialize a User object with a username and a hashed password using bcrypt.
        
        Args:
            username (str): The username for the User object.
            password (str): The password for the User object.
        
        Attributes:
            username (str): The username provided during object initialization.
            password (str): The hashed password generated using bcrypt.
        
        Note:
            The password is hashed using bcrypt's hashpw function and then decoded for storage.
        
        Returns:
            None
        """
        self.username = username
        self.password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    def check_password(self, password):
        """Check if the provided password matches the stored hashed password using bcrypt.
        
        Args:
            password (str): The password to be checked.
        
        Returns:
            bool: True if the provided password matches the stored hashed password, False otherwise.
        """
        return bcrypt.checkpw(password.encode(), self.password.encode())

def register_user(username, password):
    """
    Register a user with the provided username and password.
    
    Args:
        username (str): The username of the user to be registered.
        password (str): The password of the user to be registered.
    
    Returns:
        str: A message confirming the successful registration of the user.
    """
    return f"User {username} registered successfully."

def login(username, password):
    """Simulate a user login process.
    
    Args:
        username (str): The username of the user attempting to log in.
        password (str): The password of the user attempting to log in.
    
    Returns:
        str: A message indicating successful login along with a token for the user.
    """
    return f"User {username} logged in successfully. Here's your token."

def reset_password(username, new_password):
    """Reset the password for a specific user.
    
    Args:
        username (str): The username of the user whose password needs to be reset.
        new_password (str): The new password to set for the user.
    
    Returns:
        str: A success message confirming that the password for the specified user has been reset successfully.
    """
    return f"Password for user {username} reset successfully."
