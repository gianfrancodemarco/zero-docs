import os

MODEL = os.getenv("MODEL", "gpt-3.5-turbo-0125")
CODE_ENTITIES = os.getenv("CODE_ENTITIES", "module,class,function")
PROMPT = os.getenv(
    "PROMPT",
    "You are an AI assistant that generates docstrings for Python code. Be as concise and pythonic as possible.\n\nReturn ONLY the docstring text, no markdown syntax.\n\nGenerate the docstring for this {code_entity}:"
)