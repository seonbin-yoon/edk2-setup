import platform
import sys
from typing import Any


class Color:
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    RESET = "\033[0m"


# 현재는 안 사용됌
# BACKGROUND_COLOR = {
#    "BLACK": "\033[40m",
#    "RED": "\033[41m",
#    "GREEN": "\033[42m",
#    "YELLOW": "\033[43m",
#    "BLUE": "\033[44m",
#    "MAGENTA": "\033[45m",
#    "CYAN": "\033[46m",
#    "WHITE": "\033[47m",
# }

class Config:
    def __init__(self):
        self.color_mode: bool = True

    def toogle_color_mode(self):
        self.color_mode = not self.color_mode

def clear_screen():
    if platform.system() == "Windows":
        write("\033[2J\033[3J\033[H")
    elif platform.system() == "Linux":
        write("\033[2J\033[3J\033[H")
    else:
        raise NotImplementedError("화면 초기화를 진행하지 못했습니다.")

def write(message: Any, color: str = Color.RESET, end: str = "\n", sep: str = ""):
    if not config.color_mode:
        print(message, end=end, sep=sep)
        return

    print(
        f"{color}{message}{Color.RESET}",
        end=end,
        sep=sep,
    )

def read(message: str = "", color: str = Color.RESET):
    if message:
        write(message, color, end="")

    sys.stdout.flush()
    return sys.stdin.readline().strip()

config = Config()
