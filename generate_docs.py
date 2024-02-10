import ast
import logging
import os
import sys
import time
from openai import OpenAI
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_docstring(text):
    '''"""
    Generate docstring for the given text using OpenAI API.

    Args:
    text (str): The input text for which docstring needs to be generated.

    Returns:
    str: The generated docstring for the input text.
"""'''
    try:
        logger.info('Calling OpenAI to generate docstring...')
        start_time = time.time()
        client = OpenAI()
        chat_completion = client.chat.completions.create(messages=[{'role': 'system', 'content': "\n                    You are an AI assistant that generates docstrings Python code. Be as concise and pythonic as possible.\n                    Don't add anything you don't see in the code.\nGenerate the dostring for this piece of code:\n\n\n                    "}, {'role': 'system', 'content': text}], model='gpt-3.5-turbo-1106')
        end_time = time.time()
        logger.info(f'OpenAI call completed in {end_time - start_time:.2f} seconds')
        return chat_completion.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f'Error generating docstring: {e}')
        return ''

def update_docstrings(filename):
    """Update the docstrings in the specified Python file. 

Args:
    filename (str): The name of the Python file to update.

Returns:
    None: This function does not return anything."""
    logger.info(f'Updating docstrings in file: {filename}')
    with open(filename, 'r') as f:
        content = f.read()
    tree = ast.parse(content, filename=filename)
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            if not ast.get_docstring(node):
                start_line = node.lineno - 1
                end_line = node.body[0].lineno - 1 if node.body else node.lineno
                code_block = '\n'.join(content.split('\n')[start_line:end_line])
                generated_docstring = generate_docstring(code_block)
                if generated_docstring:
                    ast.increment_lineno(node)
                    node.body.insert(0, ast.Expr(value=ast.Constant(value=generated_docstring)))
                    logger.info(f'Added docstring for {node.name}')
    updated_code = ast.unparse(tree)
    with open(filename, 'w') as f:
        f.write(updated_code)

def get_files_from_dirs(args: list[str]):
    """
    Each arg can be a directory or a file
    For each directory, get all the py files in the directory
    """
    files = []
    for arg in args:
        if os.path.isdir(arg):
            logger.info(f'Getting files from directory: {arg}')
            for (root, _, files_) in os.walk(arg):
                for file in files_:
                    if file.endswith('.py'):
                        files.append(os.path.join(root, file))
        elif arg.endswith('.py'):
            files.append(arg)
    return files
if __name__ == '__main__':
    logging.info(f'argvs: {sys.argv}')
    files = get_files_from_dirs(sys.argv[1:])
    for filename in files:
        update_docstrings(filename)