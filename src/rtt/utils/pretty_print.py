""" pretty_print.py

Pretty print utilities.

"""

import sys
import time

def pretty_print(prefix: str, message: str):
    """ Pretty print a message. """
    sys.stdout.write(prefix)
    for chr in message:
        sys.stdout.write(chr)
        sys.stdout.flush()
        time.sleep(.01)
    print()