import os

MODEL = os.getenv("MODEL", "gpt-3.5-turbo-0125")
ZERO_DOCS_INPUT_PATHS = os.getenv("ZERO_DOCS_INPUT_PATHS", ".").split(" ")
if ZERO_DOCS_INPUT_PATHS == '/':
    raise ValueError("ZERO_DOCS_INPUT_PATHS cannot be /")

ZERO_DOCS_CODE_ENTITIES = os.getenv("CODE_ENTITIES", "module,class,function").split(",")

_prompt = """
Generate a descriptive docstring for this Python {code_entity}, including details about any parameters, return values, and exceptions raised. Use proper formatting according to PEP257 guidelines. Focus on what the {code_entity} does instead of how it does it.

Example format:

def my_func(param1, param2):
    \"\"\"Description of what my_func does.

    Args:
        param1 (type): What param1 represents.
        param2 (type): What param2 represents.

    Returns:
        type: What is returned.

    Raises:
        ExceptionType: When this exception occurs.
    \"\"\"

Include the above sections only if they apply to your specific {code_entity}
"""

PROMPT = os.getenv(
    "PROMPT",
    _prompt
)
if not PROMPT:
    PROMPT = _prompt