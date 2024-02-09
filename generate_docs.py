import ast
import logging
import os
import sys
import time

from openai import OpenAI

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def generate_docstring(text):
    # Function to generate docstring using OpenAI API
    # This function takes input `text` and returns the generated docstring
    try:
        logger.info("Calling OpenAI to generate docstring...")
        start_time = time.time()
        client = OpenAI()

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": """
                    You are an AI assistant that generates docstrings Python code. Be as concise and pythonic as possible.
                    Don't add anything you don't see in the code.\nGenerate the dostring for this piece of code:\n\n
                    """,
                },
                {
                    "role": "system",
                    "content": text
                }
            ],
            model="gpt-3.5-turbo",
        )

        end_time = time.time()
        logger.info(
            f"OpenAI call completed in {end_time - start_time:.2f} seconds")
        return chat_completion.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"Error generating docstring: {e}")
        return ""


def update_docstrings(filename):
    logger.info(f"Updating docstrings in file: {filename}")
    with open(filename, "r") as f:
        content = f.read()

    tree = ast.parse(content, filename=filename)

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            if not ast.get_docstring(node):

                start_line = node.lineno - 1
                end_line = node.body[0].lineno - \
                    1 if node.body else node.lineno
                code_block = "\n".join(content.split("\n")[
                                       start_line:end_line])
                generated_docstring = generate_docstring(code_block)

                if generated_docstring:
                    # Add the generated docstring to the node
                    ast.increment_lineno(node)
                    node.body.insert(0, ast.Expr(
                        value=ast.Constant(value=generated_docstring)))
                    logger.info(f"Added docstring for {node.name}")

    # Generate updated source code
    updated_code = ast.unparse(tree)

    # Write the updated content back to the file
    with open(filename, "w") as f:
        f.write(updated_code)


def get_files_from_dirs(args: list[str]):
    """
    Each arg can be a directory or a file
    For each directory, get all the py files in the directory
    """

    files = []
    for arg in args:
        if os.path.isdir(arg):
            logger.info(f"Getting files from directory: {arg}")
            # Scan directory for Python files
            for root, _, files_ in os.walk(arg):
                for file in files_:
                    if file.endswith(".py"):
                        files.append(os.path.join(root, file))
        else:
            if arg.endswith(".py"):
                files.append(arg)

    return files


if __name__ == "__main__":

    logging.info(f"argvs: {sys.argv}")

    files = get_files_from_dirs(sys.argv[1:])
    for filename in files:
        update_docstrings(filename)