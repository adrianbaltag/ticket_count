"""This module contains custom decorators that can be used to modify the behavior of functions."""

from functools import wraps


def remove_duplicates(func):
    """Decorator to remove duplicate lines while keeping the first occurrence."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)  # Call the original function

        if not isinstance(result, str):  # Ensure we got a valid string response
            return result

        unique_lines = []
        seen = set()

        for line in result.split("\n"):  # Process each line
            if line not in seen:
                seen.add(line)
                unique_lines.append(line)

        return "\n".join(unique_lines)  # Return cleaned text

    return wrapper
