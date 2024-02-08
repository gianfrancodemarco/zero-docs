import logging
import sys
from docstring_generator import DocstringManager
from docstring_updater import DocstringUpdater
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_files_from_args(args: list[str]):
    files = []
    for arg in args:
        if os.path.isdir(arg):
            logger.info(f"Getting files from directory: {arg}")
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

    updater = DocstringUpdater(generator=DocstringManager())

    files = get_files_from_args(sys.argv[1:])
    files = get_files_from_args(["tests/tests.py"])

    for filename in files:
        updater.update_docstrings(filename)
