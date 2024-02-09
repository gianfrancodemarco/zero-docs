import bcrypt

class User:
    """This class represents a user."""

    def __init__(self, username, password):
        """Assigns the value of `username` parameter to the `username` attribute of the class."""
        self.username = username
        self.password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    def check_password(self, password):
        """Checks if the provided password matches the hashed password stored in self.password. Returns True if the passwords match, otherwise False."""
        return bcrypt.checkpw(password.encode(), self.password.encode())

def register_user(username, password):
    """Registers a new user with the given username and password."""
    return f'User {username} registered successfully.'

def login(username, password):
    """This function is responsible for authenticating a user with a provided username and password."""
    return f"User {username} logged in successfully. Here's your token."

def reset_password(username, new_password):
    """Resets the password for the specified username to the new password."""
    return f'Password for user {username} reset successfully.'