from __future__ import annotations

import shutil
from argparse import RawTextHelpFormatter
from enum import Enum
from re import compile, split


##########
# Common #
##########
class Color:
    BLUE = "\033[0;36m"
    GREEN = "\033[0;32m"
    RED = "\033[0;31m"
    RESET = "\033[0m"
    YELLOW = "\033[1;33m"


class CustomFormatter(RawTextHelpFormatter):
    def __init__(self, prog):
        super().__init__(prog, width=max(80, shutil.get_terminal_size().columns - 2))


class StrEnum(Enum):
    def __new__(cls, value) -> StrEnum:
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    @classmethod
    def from_str(cls, value) -> StrEnum:
        for member in cls:
            if value in member.value:
                return member
        raise ValueError(f"Invalid value: '{value}'. Valid options are {cls.valid_options()}")

    @classmethod
    def valid_options(cls) -> str:
        options = [alias for member in cls for alias in member.value]
        return ", ".join(options)

    def __str__(self) -> str:
        return self.name


dre = compile(r"(\d+)")  # pre-compile for speed


def natural_sort(lst: list) -> list:
    return sorted(lst, key=lambda p: [int(s) if s.isdigit() else s.lower() for s in split(dre, p)])
