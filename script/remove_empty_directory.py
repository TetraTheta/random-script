import os
import subprocess
import sys
from pathlib import Path


def remove_empty_directory(dir: Path):
    for subdir in dir.iterdir():
        if subdir.is_dir():
            remove_empty_directory(subdir)
    try:
        dir.rmdir()
        print(f"{Fore.YELLOW}REMOVE{Style.RESET_ALL} {dir.parent}{os.sep}{Fore.YELLOW}{dir.name}{Style.RESET_ALL}")
    except OSError:
        pass


if __name__ == "__main__":
    # Install colorama if not present
    try:
        from colorama import Fore, Style
        from colorama import init as colorinit
    except ModuleNotFoundError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "colorama"])
        sys.exit(subprocess.call([sys.executable] + sys.argv))

    colorinit()

    # Parse command line
    from argparse import ArgumentParser

    cli = ArgumentParser(prog="lowercase")
    cli.add_argument("-y", "--yes", action="store_true")
    cli.add_argument("target", nargs="?", default=Path.cwd().resolve(), type=Path)

    args = cli.parse_args()

    args.target = args.target.resolve()

    if not args.target.is_dir():
        print(f"{Fore.RED}ERROR{Style.RESET_ALL} Given path '{args.target}' is not a directory")
        sys.exit(1)

    if not args.yes:
        print(f"{Fore.GREEN}TARGET{Style.RESET_ALL} {args.target}")
        result = input("Do you want to lowercase any sub directory or files of this directory? (yes/no): ")
        if result.lower() == "yes" or result.lower() == "y":
            remove_empty_directory(args.target)
        else:
            print(f"{Fore.RED}ERROR{Style.RESET_ALL} User canceled the opration")
            sys.exit(1)
    else:
        remove_empty_directory(args.target)
