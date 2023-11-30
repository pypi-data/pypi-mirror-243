import re


def snake_to_camel(string: str) -> str:
    """
    Converts string in snake case to camel case

    Args:
        string (str): string to convert

    Returns:
        str: converted string
    """
    return "".join([s.capitalize() for s in string.strip("_").strip("_").split("_")])


def camel_to_snake(string: str) -> str:
    """
    Converts a string in camel case to snake case

    Explanation here: https://stackoverflow.com/a/1176023/16797805

    Args:
        string (str): string to convert

    Returns:
        str: converted string
    """
    string = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", string)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", string).lower()
