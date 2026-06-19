import os
import platform
import sys
from typing import Any, NoReturn

import distro
import psutil

from utils import color_print
from utils._except import InitError
from utils.color_print import Color

__DISTRO: dict[tuple[str, ...], str] = {
    ("fedora", "rhel"): "RHEL",
    ("ubuntu", "debian"): "DEBIAN"
}

def get_distro() -> str:
    os = platform.system()

    if os != "Linux":
        raise InitError.UnsupportedOSError(os)

    os_distro_id = distro.id()

    for keys, value in __DISTRO.items():
        if os_distro_id.lower() in keys:
            return value
    raise InitError.UnsupportedOSError(os_distro_id)

def get_threads():
    return psutil.cpu_count(logical=True)

def get_home_path() -> str:
    path = os.path.expanduser("~")
    if path == "~":
        raise InitError.HomePathNotFoundError

    return path

def check_need_sudo() -> bool:
    if os.getuid() == 0:
        return False

    return True

def program_exit(exit_code: int = 0, message: Any = "", color: str = Color.RESET)\
    -> NoReturn:

    if message:
        color_print.write(message, color)
    sys.exit(exit_code)
