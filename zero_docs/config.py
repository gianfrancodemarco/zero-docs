import os

MODEL = os.getenv("MODEL", "gpt-3.5-turbo-0125")
ZERO_DOCS_INPUT_PATHS = os.getenv("ZERO_DOCS_INPUT_PATHS", ".").split(" ")
if ZERO_DOCS_INPUT_PATHS == '/':
    raise ValueError("ZERO_DOCS_INPUT_PATHS cannot be /")

ZERO_DOCS_CODE_ENTITIES = os.getenv("CODE_ENTITIES", "module,class,function").split(",")

_prompt = """
Generate a descriptive docstring for this Python {code_entity}, including details about any parameters, return values, and exceptions raised. Use proper formatting according to PEP257 guidelines. Focus on what the {code_entity} does instead of how it does it.

Example:

Code:
def check_password(self, password):
    return bcrypt.checkpw(password.encode(), self.password.encode())

Docstring:
\"\"\"Check if the given password is correct using bcrypt.

Args:
    password (str): The password to check.

Returns:
    bool: True if the password is correct, False otherwise.
\"\"\"

Example 2:

Code:
class User:
    def __init__(self, username, password):
        self.username = username
        self.password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    def check_password(self, password):
        return bcrypt.checkpw(password.encode(), self.password.encode())


Docstring:
\"\"\"A user of the application. A user has a username and password, and can check their password.

Attributes:
    username (str): The username of the user.
    password (str): The hashed password of the user.

Methods:
    check_password: Check if the given password is correct.
\"\"\"

Include the above sections only if they apply to your specific {code_entity}
"""

PROMPT = os.getenv(
    "PROMPT",
    _prompt
)
if not PROMPT:
    PROMPT = _prompt