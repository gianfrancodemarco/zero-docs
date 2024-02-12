import os

MODEL = os.getenv("MODEL", "gpt-3.5-turbo-0125")
ZERO_DOCS_INPUT_PATHS = os.getenv("ZERO_DOCS_INPUT_PATHS", ".").split(" ")
if ZERO_DOCS_INPUT_PATHS == '/':
    raise ValueError("ZERO_DOCS_INPUT_PATHS cannot be /")

ZERO_DOCS_CODE_ENTITIES = os.getenv("CODE_ENTITIES", "module,class,function").split(",")

_prompt = "Generate a descriptive docstring for this Python {code_entity}, including details about any parameters, return values, and exceptions raised. Use proper formatting according to PEP257 guidelines. Focus on what the function does instead of how it does it."
PROMPT = os.getenv(
    "PROMPT",
    _prompt
)
if not PROMPT:
    PROMPT = _prompt