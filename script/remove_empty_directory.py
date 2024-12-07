import os
import sys
from pathlib import Path


class Color:
    CYAN = "\033[0;36m"
    GREEN = "\033[0;32m"
    RED = "\033[0;31m"
    RESET = "\033[0m"
    YELLOW = "\033[1;33m"


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


if __name__ == "__main__":
    # Parse command line
    from argparse import ArgumentParser

    cli = ArgumentParser(prog="remove-empty-directory", description="Remove empty directories from given path")
    cli.add_argument("-y", "--yes", action="store_true", help="Skip confirmation")
    cli.add_argument("target", type=Path, default=Path.cwd().resolve(), nargs="?", help="Target directory")

    args = cli.parse_args()

    args.target = args.target.resolve()

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
