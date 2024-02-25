"""
A configuration module for generating descriptive docstrings for Python functions, classes, and modules.

Constants:
    - MODEL: The default model for docstring generation.
    - ZERO_DOCS_INPUT_PATHS: Paths for input sources.
    - ZERO_DOCS_CODE_ENTITIES: Code entities to include in docstrings.
    - FUNCTION_PROMPT: Default prompt format for generating function docstrings.
    - CLASS_PROMPT: Default prompt format for generating class docstrings.
    - MODULE_PROMPT: Default prompt format for generating module docstrings.
    
Environment Variables:
    - ZERO_DOCS_FUNCTION_PROMPT: Custom prompt for function docstrings.
    - ZERO_DOCS_CLASS_PROMPT: Custom prompt for class docstrings.
    - ZERO_DOCS_MODULE_PROMPT: Custom prompt for module docstrings.

Functions:
    - No functions in this module.

Classes:
    - No classes in this module.

Modules:
    - No modules in this module.
"""
import os

MODEL = os.getenv("MODEL", "gpt-3.5-turbo-0125")
ZERO_DOCS_INPUT_PATHS = os.getenv("ZERO_DOCS_INPUT_PATHS", ".").split(" ")
if ZERO_DOCS_INPUT_PATHS == '/':
    raise ValueError("ZERO_DOCS_INPUT_PATHS cannot be /")

ZERO_DOCS_CODE_ENTITIES = os.getenv("ZERO_DOCS_CODE_ENTITIES", "module,class,function").split(",")

FUNCTION_PROMPT = """
Generate a descriptive docstring for this Python function, including details about any parameters, return values, and exceptions raised. Use proper formatting according to PEP257 guidelines. Focus on what the function does instead of how it does it.
Only include sections that are relevant to the function. For example, if the function does not raise any exceptions, do not include an exceptions section.

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
"""

CLASS_PROMPT = """
Generate a descriptive docstring for this Python class, including details about any attributes and methods. Use proper formatting according to PEP257 guidelines. Focus on what the class does instead of how it does it.
Only include sections that are relevant to the class. For example, if the class does not have any methods, do not include a methods section

Example:

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
"""

MODULE_PROMPT = """
Generate a descriptive docstring for this Python module, including a summary of the module's contents. Use proper formatting according to PEP257 guidelines.
Only include sections that are relevant to the module. For example, if the module does not contain any classes, do not include a classes section.

Example:

Code:

class Calculator:
    def add(self,x, y):
        return x + y

    def subtract(self,x, y):
        return x - y

    def multiply(self,x, y):
        return x * y

    def divide(self,x, y):
        if y == 0:
            raise ZeroDivisionError("Division by zero is not allowed.")
        return x / y


Docstring:
\"\"\"A simple calculator module.

This module contains a class, Calculator
which can perform basic arithmetic operations.

Classes:
    Calculator: A simple calculator class.

Methods:
    add: Add two numbers.
    subtract: Subtract two numbers.
    multiply: Multiply two numbers.
    divide: Divide two numbers.

Exceptions: 

    ZeroDivisionError: Raised when attempting to divide by zero.
\"\"\"
"""

PROMPTS_MAPPING = {
    "function": os.getenv("ZERO_DOCS_FUNCTION_PROMPT") or FUNCTION_PROMPT,
    "class": os.getenv("ZERO_DOCS_CLASS_PROMPT") or CLASS_PROMPT,
    "module": os.getenv("ZERO_DOCS_MODULE_PROMPT") or MODULE_PROMPT
}