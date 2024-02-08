import os

MODEL = os.getenv("MODEL", "gpt-3.5-turbo-0125")
ZERO_DOCS_INPUT_PATHS = os.getenv("ZERO_DOCS_INPUT_PATHS", ".").split(" ")
if ZERO_DOCS_INPUT_PATHS == '/':
    raise ValueError("ZERO_DOCS_INPUT_PATHS cannot be /")

ZERO_DOCS_CODE_ENTITIES = os.getenv("CODE_ENTITIES", "module,class,function").split(",")

_prompt = "You are an AI assistant that generates docstrings for Python code. Be as concise and pythonic as possible.\n\nReturn ONLY the docstring text, no markdown syntax.\n\nGenerate the docstring for this {code_entity}:"
PROMPT = os.getenv(
    "PROMPT",
    _prompt
)
if not PROMPT:
    PROMPT = _prompt