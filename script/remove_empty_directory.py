import os
import sys
from argparse import ArgumentParser
from pathlib import Path

from library.python_lib import Color, CustomFormatter  # noqa: E402

# This script requires > 3.12 (Path.is_junction())
if sys.version_info < (3, 12):
    print(f"{Color.RED}ERROR  {Color.RESET} This script requires Python version above 3.12")
    sys.exit(1)

if sys.platform == "win32":
    exclusion = [
        r"%AppData%\\Microsoft",
        r"%LocalAppData%\\Microsoft",
    ]
else:
    exclusion = []
exclusion = [Path(os.path.expandvars(path)).resolve() for path in exclusion]


class RemoveEmptyDirectoryNamespace:
    target: str | Path = Path.cwd()
    yes: bool = False


def remove_empty_directory(dir: Path, top_level: Path):
    try:
        if not dir.is_dir():
            return

        is_junction = dir.is_junction() if sys.platform == "win32" else False
        is_symlink = dir.is_symlink()

        if is_symlink or is_junction:
            print(f"{Color.BLUE}SYMLINK{Color.RESET} {dir}")
            return

        for subdir in dir.iterdir():
            if subdir.is_dir():
                try:
                    if any(subdir.resolve().is_relative_to(exc) for exc in exclusion):
                        print(f"{Color.BLUE}SKIP   {Color.RESET} {subdir}")
                        continue
                except OSError:
                    pass
            remove_empty_directory(subdir, top_level)

        if dir != top_level:
            try:
                dir.rmdir()
                print(f"{Color.YELLOW}REMOVE {Color.RESET} {dir.parent}{os.sep}{Color.YELLOW}{dir.name}{Color.RESET}")
            except OSError:
                pass

    except PermissionError:
        print(f"{Color.RED}PERMERR{Color.RESET} {dir}")
    except NotADirectoryError:
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
    print(f"{Color.RED}ERROR  {Color.RESET} Given path '{args.target}' is not a directory")
    sys.exit(1)

if not args.yes:
    print(f"{Color.GREEN}TARGET{Color.RESET} {args.target}")
    result = input("Do you want to remove empty directories from this path? (yes/no): ")
    if result.lower() == "yes" or result.lower() == "y":
        remove_empty_directory(args.target, args.target)
    else:
        print(f"{Color.RED}CANCEL {Color.RESET} User canceled the operation")
        sys.exit(1)
else:
    remove_empty_directory(args.target, args.target)
