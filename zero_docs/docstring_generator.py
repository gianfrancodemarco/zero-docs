"""
Generate docstring for the function to call OpenAI to generate a docstring based on given code and code entity.
"""
import logging
import time

from openai import OpenAI

from zero_docs.config import MODEL, PROMPT
from zero_docs.enums import CodeEntity

logger = logging.getLogger(__name__)


class DocstringManager:
    """
    Generate docstring for the function to call OpenAI to generate a docstring based on given code and code entity.
    """

    def generate(
        self,
        code: str,
        code_entity: CodeEntity
    ) -> str:
        """
        Generate docstring for the function to call OpenAI to generate a docstring based on given code and code entity.
        """
        logger.info("Calling OpenAI to generate docstring...")
        start_time = time.time()
        client = OpenAI()
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": PROMPT.format(code_entity=code_entity.value)
                },
                {
                    "role": "user",
                    "content": code
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
        """
        Converts the given docstring to use triple double quotes and applies the specified number of indented blocks.
        """

        docstring = docstring.strip().replace("'''", '"""')

        if not docstring.startswith('"""'):
            docstring = f'"""\n{docstring}\n"""'

        docstring = docstring.replace("\n", "\n" + "    " * num_indented_blocks)

        return docstring
