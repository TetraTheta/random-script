import shutil
import sys
from argparse import ArgumentParser, ArgumentTypeError, RawTextHelpFormatter
from pathlib import Path

class Color:
    BLUE = "\033[0;36m"
    GREEN = "\033[0;32m"
    RED = "\033[0;31m"
    RESET = "\033[0m"
    YELLOW = "\033[1;33m"

class CustomFormatter(RawTextHelpFormatter):
    def __init__(self, prog):
        super().__init__(prog, width=max(80, shutil.get_terminal_size().columns - 2))

def renumber(dir: Path, ext: str, digit: int, start: int):
    exts = [f".{e.strip().lower()}" for e in ext.split(",")]
    files = sorted([f for f in dir.iterdir() if f.suffix.lower() in exts and f.is_file()], key=lambda x: x.name.lower())

    if not files:
        print(f"{Color.RED}ERROR{Color.RESET} There is no file with extension(s) {exts} in '{dir}'.")
        return

    temp_files = []
    for file in files:
        temp_name = f"rntmp-{file.name}"
        temp_path = dir / temp_name
        file.rename(temp_path)
        temp_files.append((file.name, temp_path))

    for i, (original_name, file) in enumerate(temp_files, start=start):
        new_name = f"{str(i).zfill(digit)}{file.suffix.lower()}"
        new_path = dir / new_name
        file.rename(new_path)
        print(f"{Color.YELLOW}RENAME{Color.RESET} {original_name} → {new_name}")

    print(f"{Color.GREEN}INFO{Color.RESET} Renumber complete.")

def check_non_negative(value) -> int:
    try:
        number = int(value)
        if not number >= 0:
            raise ArgumentTypeError(f"{number} is not non-negative integer ({number} >= 0)")
        else:
            return number
    except ValueError:
        raise ArgumentTypeError(f"{value} is not a number")

def check_positive(value) -> int:
    try:
        number = int(value)
        if not number > 0:
            raise ArgumentTypeError(f"{number} must be positive number ({number} > 0)")
        else:
            return number
    except ValueError:
        raise ArgumentTypeError(f"{value} is not a number")

##########
#  MAIN  #
##########
cli = ArgumentParser(prog="renumber", description="Rename image files in a directory with sequential numbering.", formatter_class=CustomFormatter)
cli.add_argument("-e", "--ext", type=str, default="webp", choices=["bmp", "gif", "jpg", "png", "webp"], help="Extension(s) of image files to rename, separated by commas.\n(default: webp)")
cli.add_argument("-s", "--start", type=check_non_negative, default=1, help="Starting number for renaming. Must be non-negative integer.\n(default: 1)")
cli.add_argument("-d", "--digit", type=check_positive, default=3, help="Number of digits for renamed files.\n(default: 3)")
cli.add_argument("-y", "--yes", action="store_true", help="Skip confirmation\n(default: False)")
cli.add_argument("target", default=str(Path.cwd()), nargs="?", help=f"Target directory.\n(default: {Path.cwd()})")

args = cli.parse_args()

args.target = Path(args.target).resolve()

if not args.target.is_dir():
    print(f"{Color.RED}ERROR{Color.RESET} Given path '{args.target}' is not a directory")
    sys.exit(1)

if not args.yes:
    print(f"{Color.GREEN}TARGET{Color.RESET} {args.target}")
    result = input("Do you want to renumber image files of this directory? (yes/no): ")
    if result.lower() == "yes" or result.lower() == "y":
        renumber(args.target, args.ext, args.digit, args.start)
    else:
        print(f"{Color.RED}ERROR{Color.RESET} User canceled the opration")
        sys.exit(1)
else:
    renumber(args.target, args.ext, args.digit, args.start)
