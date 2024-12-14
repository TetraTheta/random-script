import shutil
from argparse import RawTextHelpFormatter


class Color:
    BLUE = "\033[0;36m"
    GREEN = "\033[0;32m"
    RED = "\033[0;31m"
    RESET = "\033[0m"
    YELLOW = "\033[1;33m"


class CustomFormatter(RawTextHelpFormatter):
    def __init__(self, prog):
        super().__init__(prog, width=max(80, shutil.get_terminal_size().columns - 2))
