"""
An enumeration of different code entities: FUNCTION, CLASS, MODULE.
"""
from enum import Enum


class CodeEntity(Enum):
    """
    An enumeration of different code entities: FUNCTION, CLASS, MODULE.
    """
    FUNCTION = "function"
    CLASS = "class"
    MODULE = "module"
