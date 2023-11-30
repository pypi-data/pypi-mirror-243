"""Utility functions for day-to-day Python coding."""
from re import fullmatch


def is_valid_python_name(name: str) -> bool:
    """Validate Python name given as string.

    Uses the regex `^[a-zA-Z_][a-zA-Z0-9_]*$` to check if a string would pass as a
    validate Python object identifier.

    Args:
    ----
        name: Name to validate.

    Returns:
    -------
        Boolean flagging whether or not `name` passes validation.
    """
    py_name_pattern = "^[a-zA-Z_][a-zA-Z0-9_]*$"
    return True if fullmatch(py_name_pattern, name) else False
