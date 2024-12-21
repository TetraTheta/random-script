import shutil
import sys
import tkinter as tk
from argparse import ArgumentParser, ArgumentTypeError
from enum import Enum
from pathlib import Path

from library.python_gui_lib import ScrollableListbox, TooltipLabel
from library.python_lib import Color, CustomFormatter


# ==== Data ====
# fmt: off
class CropPosition(Enum): BOTTOM = 1; CENTER = 2; FULL = 3  # noqa:E701,E702
class Game(Enum): TOF = "tof"; WW = "ww"  # noqa:E701,E702
class Operation(Enum): ALL = 1; BACKGROUND = 2; CENTER = 3; CREATE_DIRECTORY = 4; FOREGROUND_0 = 5; FOREGROUND_1 = 6; FOREGROUND_2 = 7; FOREGROUND_3 = 8; FOREGROUND_4 = 9; FULL = 10  # noqa:E701,E702

class GameDefinition:
    UID_AREA: str = ""
    UID_POS: str = ""
    CROP_POS: CropPosition = CropPosition.FULL
    CROP_HEIGHT: int = 0

    def __init__(self, game: Game, op: Operation):
        if game == Game.TOF:
            self.UID_AREA = "144:22"
            self.UID_POS = "1744:1059"
            if op == Operation.BACKGROUND: self.CROP_POS = CropPosition.BOTTOM; self.CROP_HEIGHT = 330  # noqa:E701,E702
            elif op == Operation.CENTER: self.CROP_POS = CropPosition.CENTER; self.CROP_HEIGHT = 200  # noqa:E701,E702
            elif op == Operation.FOREGROUND_0: self.CROP_POS = CropPosition.BOTTOM; self.CROP_HEIGHT = 280  # noqa:E701,E702
            elif op == Operation.FOREGROUND_1: self.CROP_POS = CropPosition.BOTTOM; self.CROP_HEIGHT = 420  # noqa:E701,E702
            elif op == Operation.FOREGROUND_2: self.CROP_POS = CropPosition.BOTTOM; self.CROP_HEIGHT = 495  # noqa:E701,E702
            elif op == Operation.FOREGROUND_3: self.CROP_POS = CropPosition.BOTTOM; self.CROP_HEIGHT = 570  # noqa:E701,E702
            elif op == Operation.FOREGROUND_4: self.CROP_POS = CropPosition.BOTTOM; self.CROP_HEIGHT = 645  # noqa:E701,E702
            elif op == Operation.FULL: self.CROP_POS = CropPosition.FULL; self.CROP_HEIGHT = 0  # noqa:E701,E702
        elif game == Game.WW:
            self.UID_AREA = "144:22"
            self.UID_POS = "1744:1059"
            if op == Operation.BACKGROUND: self.CROP_POS = CropPosition.BOTTOM; self.CROP_HEIGHT = 360  # noqa:E701,E702
            elif op == Operation.CENTER: self.CROP_POS = CropPosition.CENTER; self.CROP_HEIGHT = 200  # noqa:E701,E702
            elif op == Operation.FOREGROUND_0: self.CROP_POS = CropPosition.BOTTOM; self.CROP_HEIGHT = 310  # noqa:E701,E702
            elif op == Operation.FOREGROUND_1: self.CROP_POS = CropPosition.BOTTOM; self.CROP_HEIGHT = 420  # noqa:E701,E702
            elif op == Operation.FOREGROUND_2: self.CROP_POS = CropPosition.BOTTOM; self.CROP_HEIGHT = 505  # noqa:E701,E702
            elif op == Operation.FOREGROUND_3: self.CROP_POS = CropPosition.BOTTOM; self.CROP_HEIGHT = 580  # noqa:E701,E702
            elif op == Operation.FOREGROUND_4: self.CROP_POS = CropPosition.BOTTOM; self.CROP_HEIGHT = 665  # noqa:E701,E702
            elif op == Operation.FULL: self.CROP_POS = CropPosition.FULL; self.CROP_HEIGHT = 0  # noqa:E701,E702


def path_bg(dir: Path) -> Path: return dir / "CS-Background"
def path_center(dir: Path) -> Path: return dir / "CS-Center"
def path_fg0(dir: Path) -> Path: return dir / "CS-Foreground-0"
def path_fg1(dir: Path) -> Path: return dir / "CS-Foreground-1"
def path_fg2(dir: Path) -> Path: return dir / "CS-Foreground-2"
def path_fg3(dir: Path) -> Path: return dir / "CS-Foreground-3"
def path_fg4(dir: Path) -> Path: return dir / "CS-Foreground-4"
def path_full(dir: Path) -> Path: return dir / "CS-Full"
# fmt: on
# ==== Data END ====


class ConvertScreenshotNamespace:
    definition: GameDefinition
    game: Game
    operation: Operation
    target: str | Path


def check_requirements():
    missing_components = []
    if not (is_gid_present or is_magick_present):
        missing_components.append("      - Either 'get-image-dimension' or 'magick' is required for getting dimension of image.")
        missing_components.append(f"        Download Get-Image-Dimension from {Color.BLUE}https://github.com/TetraTheta/Get-Image-Dimension/releases{Color.RESET}")
        missing_components.append(f"        Download ImageMagick from {Color.BLUE}https://imagemagick.org/script/download.php{Color.RESET}")

    if not is_ffmpeg_present:
        missing_components.append("      - 'ffmpeg' is required for converting image.")
        missing_components.append(f"        Downlaod FFmpeg from {Color.BLUE}https://www.gyan.dev/ffmpeg/builds/{Color.RESET}")

    if missing_components:
        print(f"{Color.RED}FATAL{Color.RESET} The following requirements are missing:")
        print("\n".join(missing_components))
        sys.exit(1)


def create_directory(dir: Path):
    try:
        dir.mkdir()
    except FileExistsError:
        print(f"{Color.RED}ERROR{Color.RESET} Directory '{dir}' already exists")


def game_type(value: str) -> Game:
    try:
        return Game(value)
    except ValueError:
        raise ArgumentTypeError(f"invalid choice: '{value}' (choose from '{Game.TOF.value}', '{Game.WW.value}')")


def operation_type(value: str) -> Operation:
    map = {
        Operation.ALL: ["all", "a"],
        Operation.BACKGROUND: ["background", "bg", "b"],
        Operation.CENTER: ["center", "c"],
        Operation.CREATE_DIRECTORY: ["createdirectory", "create-directory", "create_directory", "cd"],
        Operation.FOREGROUND_0: ["foreground0", "foreground-0", "foreground_0", "fg0"],
        Operation.FOREGROUND_1: ["foreground1", "foreground-1", "foreground_0", "fg1"],
        Operation.FOREGROUND_2: ["foreground2", "foreground-2", "foreground_0", "fg2"],
        Operation.FOREGROUND_3: ["foreground3", "foreground-3", "foreground_0", "fg3"],
        Operation.FOREGROUND_4: ["foreground4", "foreground-4", "foreground_0", "fg4"],
        Operation.FULL: ["full", "f"],
    }
    for operation, aliases in map.items():
        if value in aliases:
            return operation

    raise ArgumentTypeError(f"invalid choice: '{value}' (choose from {', '.join([f"\'{alias}\'" for aliases in map.values() for alias in aliases])})")


# ==== GUI ====


##########
#  MAIN  #
##########
is_cwebp_present = shutil.which("cwebp") is not None
is_ffmpeg_present = shutil.which("ffmpeg") is not None
is_gid_present = shutil.which("get-image-dimension") is not None
is_magick_present = shutil.which("magick") is not None

check_requirements()

help_game = "Game that the screenshot(s) take from\n- tof: Tower of Fantasy\n- ww: Wuthering Waves"
help_operation = "Operation to do to the screenshot(s)\n- all(a): Do every other operations.\n          Screenshots must be in directories created by 'create-directory'.\n- background(bg)\n- center(c)\n- create-directory(cd)\n- foreground-0(fg0)\n- foreground-1(fg1)\n- foreground-2(fg2)\n- foreground-3(fg3)\n- foreground-4(fg4)\n- full(f)"

cli = ArgumentParser(prog="convert_screenshot", description="Crop and resize game screenshots", formatter_class=CustomFormatter)
cli.add_argument("-g", "--game", type=game_type, metavar="{tof, ww}", help=help_game)
cli.add_argument("-o", "--operation", type=operation_type, metavar="{a, bg, c, cd, fg0, fg1, fg2, fg3, fg4, f}", help=help_operation)
cli.add_argument("target", default=str(Path.cwd()), nargs="?", help=f"Target directory\n(default: {Path.cwd()})")  # I can't use 'type=Path' because it can't handle '.' being passed to it

args = cli.parse_args(namespace=ConvertScreenshotNamespace)
args.definition = GameDefinition(args.game, args.operation)
args.target = Path(args.target).resolve()

if not args.target.is_dir():
    print(f"{Color.RED}ERROR{Color.RESET} Given path '{args.target}' is not a directory")
    sys.exit(1)

# Predefine target directory
dir_bg = path_bg(args.target)
dir_center = path_center(args.target)
dir_fg0 = path_fg0(args.target)
dir_fg1 = path_fg1(args.target)
dir_fg2 = path_fg2(args.target)
dir_fg3 = path_fg3(args.target)
dir_fg4 = path_fg4(args.target)
dir_full = path_full(args.target)

# Process ALL and CREATE_DIRECTORY
if args.operation == Operation.ALL:
    dirok_bg = dir_bg.is_dir()
    dirok_center = dir_center.is_dir()
    dirok_fg0 = dir_fg0.is_dir()
    dirok_fg1 = dir_fg1.is_dir()
    dirok_fg2 = dir_fg2.is_dir()
    dirok_fg3 = dir_fg3.is_dir()
    dirok_fg4 = dir_fg4.is_dir()
    dirok_full = dir_full.is_dir()
    if not (dirok_bg and dirok_center and dirok_fg0 and dirok_fg1 and dirok_fg2 and dirok_fg3 and dirok_fg4 and dirok_full):
        print(f"{Color.RED}ERROR{Color.RESET} At least one of these directory should be present:")
        print(f"- {Color.GREEN if dirok_bg else Color.RED} {dir_bg}{Color.RESET}")
        print(f"- {Color.GREEN if dirok_center else Color.RED} {dir_center}{Color.RESET}")
        print(f"- {Color.GREEN if dirok_fg0 else Color.RED} {dir_fg0}{Color.RESET}")
        print(f"- {Color.GREEN if dirok_fg1 else Color.RED} {dir_fg1}{Color.RESET}")
        print(f"- {Color.GREEN if dirok_fg2 else Color.RED} {dir_fg2}{Color.RESET}")
        print(f"- {Color.GREEN if dirok_fg3 else Color.RED} {dir_fg3}{Color.RESET}")
        print(f"- {Color.GREEN if dirok_fg4 else Color.RED} {dir_fg4}{Color.RESET}")
        print(f"- {Color.GREEN if dirok_full else Color.RED} {dir_full}{Color.RESET}")
        sys.exit(1)

if args.operation == Operation.CREATE_DIRECTORY:
    create_directory(dir_bg)
    create_directory(dir_center)
    create_directory(dir_fg0)
    create_directory(dir_fg1)
    create_directory(dir_fg2)
    create_directory(dir_fg3)
    create_directory(dir_fg4)
    create_directory(dir_full)
    print(f"{Color.GREEN}DONE{Color.RESET} Directories are created at '{args.target}'")
    sys.exit(0)


# GUI
root_window = tk.Tk()
root_window.geometry("500x465")
root_window.resizable(False, False)
label = TooltipLabel(root=root_window)
listbox = ScrollableListbox(root=root_window)
button_close = tk.Button()

root_window.mainloop()
