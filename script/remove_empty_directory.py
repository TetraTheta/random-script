import os
import sys
from argparse import ArgumentParser
from pathlib import Path
import stat

from library.python_lib import Color, CustomFormatter  # noqa: E402


exclusion = [
    r"%AppData%\\Microsoft",
    r"%LocalAppData%\\Microsoft",
]
exclusion = [Path(os.path.expandvars(path)).resolve() for path in exclusion]


class RemoveEmptyDirectoryNamespace:
    target: str | Path
    yes: bool


def remove_empty_directory(dir: Path, top_level: Path):
    try:
        if not dir.is_dir():
            return

        is_junction = stat.S_ISLNK(os.stat(dir, follow_symlinks=False).st_mode)
        is_symlink = dir.is_symlink()

        if is_symlink or is_junction:
            print(f"{Color.BLUE}SYMLNK{Color.RESET} {dir}")
            return

        for subdir in dir.iterdir():
            if subdir.is_dir():
                if any(subdir.resolve().is_relative_to(exc) for exc in exclusion):
                    print(f"{Color.BLUE}SKIP  {Color.RESET} {subdir}")
                    continue
            remove_empty_directory(subdir, top_level)

        if dir != top_level:
            try:
                dir.rmdir()
                print(f"{Color.YELLOW}REMOVE{Color.RESET} {dir.parent}{os.sep}{Color.YELLOW}{dir.name}{Color.RESET}")
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
    remove_empty_directory(args.target, args.target)
