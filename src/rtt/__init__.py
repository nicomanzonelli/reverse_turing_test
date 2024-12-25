""" __init__.py


"""

__version__ = "0.1.1"

from .ui import ReverseTuringTestUI

__all__ = ["ReverseTuringTestUI"]

def main():
    try:
        ReverseTuringTestUI().cmdloop()

    except KeyboardInterrupt:
        return