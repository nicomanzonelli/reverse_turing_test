""" get_token.py

This module contains functions to retrieve a HuggingFace token from the user.

"""

from pwinput import pwinput

def get_token(prompt: str) -> str | None:
    """
    This function retrieves a HF token from the user, and ensures they only
    include printable ascii characters.
    Args: prompt (str)
    Returns: token (str)
    """
    password = pwinput(prompt=prompt)

    if (not password.isprintable()) or (0 == len(password)):
        print("Invalid password entered.\n"
              "Password must contain printable ascii characters only\n")
        return None

    else:
        return password
    