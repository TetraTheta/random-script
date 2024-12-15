import os
import sys
from argparse import ArgumentParser
from pathlib import Path

from library.python_lib import Color, CustomFormatter  # noqa: E402


class LowercaseNamespace:
    target: str | Path
    yes: bool


def lowercase(dir: Path):
    items = sorted(Path(dir).rglob("*"), key=lambda p: len(p.parts), reverse=True)
    for item in items:
        new_name = item.name.lower()
        if item.name != new_name:
            new_path = item.with_name(new_name)
            print(f"{Color.YELLOW}RENAME{Color.RESET} {item.parent}{os.sep}{{{Color.YELLOW}{item.name}{Color.RESET} → {Color.YELLOW}{new_name}{Color.RESET}}}")
            item.rename(new_path)


##########
#  MAIN  #
##########
cli = ArgumentParser(prog="lowercase", description="Convert uppercase characters to lowercase in name of file or directory", formatter_class=CustomFormatter)
cli.add_argument("-y", "--yes", action="store_true", help="Skip confirmation\n(default: False)")
cli.add_argument("target", default=str(Path.cwd()), nargs="?", help=f"Target directory\n(default: {Path.cwd()})")  # I can't use 'type=Path' because it can't handle '.' being passed to it

args = cli.parse_args(namespace=LowercaseNamespace())

args.target = Path(args.target).resolve()

if not args.target.is_dir():
    print(f"{Color.RED}ERROR{Color.RESET} Given path '{args.target}' is not a directory")
    sys.exit(1)

if not args.yes:
    print(f"{Color.GREEN}TARGET{Color.RESET} {args.target}")
    result = input("Do you want to lowercase any sub directory or files of this directory? (yes/no): ")
    if result.lower() == "yes" or result.lower() == "y":
        lowercase(args.target)
    else:
        print(f"{Color.RED}ERROR{Color.RESET} User canceled the opration")
        sys.exit(1)
else:
    lowercase(args.target)
