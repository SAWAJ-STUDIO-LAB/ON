import os


def get_env(name, default=""):
    """
    Retrieve an environment variable by name, defaulting if not found.

    Args:
        name (str): Name of the environment variable.
        default (str, optional): Default value if not found. Defaults to "".
    
    Returns:
        str: The value of the environment variable or default.
    """
    return os.environ.get(name, default).strip()
