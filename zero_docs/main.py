import logging
import os

from zero_docs.config import ZERO_DOCS_INPUT_PATHS
from zero_docs.docstring_generator import DocstringManager
from zero_docs.docstring_updater import DocstringUpdater

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_files(args: list[str]):
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

    updater = DocstringUpdater(generator=DocstringManager())

    files = get_files(ZERO_DOCS_INPUT_PATHS)

    for filename in files:
        updater.update_docstrings(filename)
