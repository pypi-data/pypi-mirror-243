import importlib
from typing import Any


def import_class(module: str, classname: str) -> Any:
    """
    Function to import a class in a module.

    Useful to do dynamic imports based on configuration files.

    Args:
        module (str): module name (full dotted path) relative to the place where the function is called
        classname (str): class name

    Returns:
        Any: class object ready to be instantiated
    """
    return getattr(importlib.import_module(module), classname)
