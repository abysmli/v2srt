# -*- coding: utf-8 -*-

"""
Utility functions for the v2srt application, including colored output.
"""

try:
    from tqdm import tqdm
    TQDM_AVAILABLE = True
except ImportError:
    TQDM_AVAILABLE = False

class Colors:
    """ANSI color codes for console output."""
    OKGREEN = '\033[92m'
    INFO = '\033[96m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def cprint(color, *args, **kwargs):
    """Prints text in a specified color."""
    print(color, end="")
    print(*args, **kwargs)
    print(Colors.ENDC, end="")
