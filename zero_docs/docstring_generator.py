"""A module for managing the generation and polishing of docstrings using the OpenAI API.

This module contains a class, DocstringManager, which provides functionality to generate and format docstrings for given code snippets using the OpenAI API.

Attributes: None

Methods:
    generate: Generate a docstring for a given code snippet using the OpenAI API.
    polish: Format and adjust the indentation of a given docstring.

Exceptions: None
"""
import logging
import time

from openai import OpenAI
from textwrap import dedent

from zero_docs.config import MODEL, PROMPTS_MAPPING
from zero_docs.enums import CodeEntity

logger = logging.getLogger(__name__)


class DocstringManager:
    """A manager for generating and polishing docstrings using the OpenAI API.
    
    Attributes: None
    
    Methods:
        generate: Generate a docstring for a given code snippet using the OpenAI API.
        polish: Format and adjust the indentation of a given docstring.
    """

    def generate(
        self,
        code: str,
        code_entity: CodeEntity
    ) -> str:
        """Generate a docstring for a given code snippet using the OpenAI API.
        
        Args:
            code (str): The code snippet for which a docstring is to be generated.
            code_entity (CodeEntity): An enum representing the type of code entity for which the docstring is being generated.
        
        Returns:
            str: The generated docstring for the provided code snippet.
        
        The function logs the information about calling the OpenAI API to generate the docstring and the time taken for the API call to complete. It constructs a request to the OpenAI API by providing messages with code prompts and code content, then retrieves and returns the generated docstring from the API response.
        """
        logger.info("Calling OpenAI to generate docstring...")
        start_time = time.time()
        client = OpenAI()

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": PROMPTS_MAPPING.get(code_entity.value)
                },
                {
                    "role": "user",
                    "content": "\n".join([
                        "Code:",
                        code,
                        "",
                        "Docstring:",
                        ""
                    ])
                }
            ],
            model=MODEL
        )

        end_time = time.time()
        logger.info(
            f"OpenAI call completed in {end_time - start_time:.2f} seconds")
        docstring = chat_completion.choices[0].message.content.strip()
        return docstring

    def polish(
        self,
        docstring: str,
        num_indented_blocks: int
    ) -> str:
        """Format and adjust the indentation of a given docstring.
        
        Args:
            docstring (str): The original docstring to format.
            num_indented_blocks (int): The number of additional indentations to apply within the docstring.
        
        Returns:
            str: The formatted and indented docstring.
        
        The function adjusts the indentation of the docstring by replacing certain patterns with corresponding replacements defined in the function. It also ensures the docstring is enclosed within triple quotes and appropriately indented based on the specified number of additional indented blocks.
        """

        docstring = docstring.strip()
        replaces = {
            "'''": '"""',
            "```plaintext": '"""',
            "```": '"""',
            "Docstring:\n": "",
            "\n": "\n" + "    " * num_indented_blocks
        }

        for old, new in replaces.items():
            docstring = docstring.replace(old, new)
        docstring = docstring.strip()

        if not docstring.startswith('"""'):
            docstring = f'"""\n{docstring}\n"""'

        return docstring
