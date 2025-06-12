from argparse import ArgumentParser, RawTextHelpFormatter
import shutil
from tkinter import Tk
import base64


class Color:
    BLUE = "\033[0;36m"
    GREEN = "\033[0;32m"
    RED = "\033[0;31m"
    RESET = "\033[0m"
    YELLOW = "\033[1;33m"


class CustomFormatter(RawTextHelpFormatter):
    def __init__(self, prog):
        super().__init__(prog, width=max(80, shutil.get_terminal_size().columns - 2))


class Base64Namespace:
    input: str


def decode(input: str):
    print("decode")
    print(input)


def encode(input: str):
    print("encode")
    print(input)


cli = ArgumentParser(prog="base64", description="Encode or Decode BASE64 string", formatter_class=CustomFormatter)
cli_sub = cli.add_subparsers(dest="command", required=True)

cli_decode = cli_sub.add_parser("decode", help="Decode BASE64 string", aliases=["d"])
cli_decode.add_argument("input", type=str, help="Input string")
cli_decode.set_defaults(func=lambda args: decode(args.input))

cli_encode = cli_sub.add_parser("encode", help="Encode BASE64 string", aliases=["e"])
cli_encode.add_argument("input", type=str, help="Input string")
cli_encode.set_defaults(func=lambda args: encode(args.input))

args = cli.parse_args(namespace=Base64Namespace())
args.func(args)

# if __name__ == "__main__":
#     args = cli.parse_args()
#     args.func(args)

# Get clipboard string
# r = Tk()
# r.withdraw()
# c = r.clipboard_get()
# r.destroy()
# print(c)
