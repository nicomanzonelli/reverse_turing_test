""" get_user_input.py

This module contains functions to retrieve user input from the user.

"""

def get_user_input(prompt: str) -> str | None:
    """
    This function retrieves user input from the user, and ensures they only 
    include printable ascii characters.
    Args: prompt (str)
    Returns: user_input (str)
    """
    while True:
        user_input = input(prompt)

        if (not user_input.isprintable()) or (0 == len(user_input)):
            print("\nEntered invalid input."
                "\nInput must contain printable ascii characters only.\n")
            continue

        else:
            return user_input