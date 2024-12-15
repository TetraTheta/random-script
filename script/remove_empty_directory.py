import os
import sys
from argparse import ArgumentParser
from pathlib import Path

from library.python_lib import Color, CustomFormatter  # noqa: E402


class RemoveEmptyDirectoryNamespace:
    target: str | Path
    yes: bool


def remove_empty_directory(dir: Path, top_level: Path = None):
    if top_level is None:
        top_level = dir

    for subdir in dir.iterdir():
        if subdir.is_dir():
            remove_empty_directory(subdir, top_level)

    if dir != top_level:
        try:
            dir.rmdir()
            print(f"{Color.YELLOW}REMOVE{Color.RESET} {dir.parent}{os.sep}{Color.YELLOW}{dir.name}{Color.RESET}")
        except OSError:
            pass


##########
#  MAIN  #
##########
cli = ArgumentParser(prog="remove-empty-directory", description="Remove empty directories from given path", formatter_class=CustomFormatter)
cli.add_argument("-y", "--yes", action="store_true", help="Skip confirmation\n(default: False)")
cli.add_argument("target", default=str(Path.cwd()), nargs="?", help=f"Target directory\n(default: {Path.cwd()})")  # I can't use 'type=Path' because it can't handle '.' being passed to it

args = cli.parse_args(namespace=RemoveEmptyDirectoryNamespace)

args.target = Path(args.target).resolve()

if not args.target.is_dir():
    print(f"{Color.RED}ERROR{Color.RESET} Given path '{args.target}' is not a directory")
    sys.exit(1)

if not args.yes:
    print(f"{Color.GREEN}TARGET{Color.RESET} {args.target}")
    result = input("Do you want to lowercase any sub directory or files of this directory? (yes/no): ")
    if result.lower() == "yes" or result.lower() == "y":
        remove_empty_directory(args.target)
    else:
        print(f"{Color.RED}ERROR{Color.RESET} User canceled the opration")
        sys.exit(1)
else:
    remove_empty_directory(args.target)
