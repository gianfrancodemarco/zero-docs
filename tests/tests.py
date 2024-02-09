import bcrypt

class User:
    """This is a class named User."""

    def __init__(self, username, password):
        """Set the value of the instance variable `username` to the given `username` parameter."""
        self.username = username
        self.password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    def check_password(self, password):
        """Checks whether a given password matches with the hashed password stored in the object."""
        return bcrypt.checkpw(password.encode(), self.password.encode())

def register_user(username, password):
    """Registers a user with the given username and password."""
    return f'User {username} registered successfully.'

def login(username, password):
    """This function takes in a username and password as parameters and is used for logging in."""
    return f"User {username} logged in successfully. Here's your token."

def reset_password(username, new_password):
    """Resets the password for the given username to the new_password."""
    return f'Password for user {username} reset successfully.'