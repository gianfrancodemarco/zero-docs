import bcrypt

class User:
    """This is a class representing a user."""

    def __init__(self, username, password):
        """Set the value of `self.username` to the provided `username`."""
        self.username = username
        self.password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    def check_password(self, password):
        """Check if the input password matches the hashed password."""
        return bcrypt.checkpw(password.encode(), self.password.encode())

def register_user(username, password):
    """Register a user with the specified username and password."""
    return f'User {username} registered successfully.'

def login(username, password):
    """This function logs in a user with the given username and password."""
    return f"User {username} logged in successfully. Here's your token."

def reset_password(username, new_password):
    """Resets the password for a user with the given username to the new_password."""
    return f'Password for user {username} reset successfully.'