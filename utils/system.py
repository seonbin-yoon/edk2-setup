import os
import platform

import distro
import psutil

from utils._except import InitError

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
