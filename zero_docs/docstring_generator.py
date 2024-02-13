import logging
import time

from openai import OpenAI
from textwrap import dedent

from zero_docs.config import MODEL, PROMPT
from zero_docs.enums import CodeEntity

logger = logging.getLogger(__name__)


class DocstringManager:

    def generate(
        self,
        code: str,
        code_entity: CodeEntity
    ) -> str:
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
                    "content": dedent(f"""
                        Code:
                        {code}

                        Docstring:
                    """)
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

        docstring = docstring.strip().replace("'''", '"""')

        if not docstring.startswith('"""'):
            docstring = f'"""\n{docstring}\n"""'

        docstring = docstring.replace("\n", "\n" + "    " * num_indented_blocks)

        return docstring
