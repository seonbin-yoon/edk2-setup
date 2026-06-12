import configparser
import os
import sys
from typing import cast

from system import edk2, qemu
from utils import color_print, datatype, system
from utils.color_print import Color
from utils.functions import program_exit


def show_message():
    color_print.write(__COMMANDS, Color.YELLOW, end="\n\n")

def get_config() -> datatype.Config:
    config = configparser.ConfigParser()

    file = config.read("user.cfg")
    if not file:
        raise FileNotFoundError

    detail = config["Config"]
    return cast(datatype.Config, dict(detail))

def processing_config(config: datatype.Config):
    for key, value in config.items():
        value = cast(str, value)
        if "!Home" in value:
            new_value = value.replace("!Home", contexts.home)
            config[key] = new_value

    if config["max_concurrent_thread_number"]:
        threads = system.get_threads()
        if threads is None:
            color_print.write("논리 쓰레드 갯수를 알 수 없습니다.\n" \
            "1로 사용합니다.", Color.RED)
            threads = 0
        config["max_concurrent_thread_number"] = (threads * 2) + 1

def check_error(result: bool):
    if result:
        color_print.write("작업을 성공적으로 완료 했습니다.", Color.BLUE)

try:
    contexts = datatype.Contexts(
        config=get_config(),
        distro=system.get_distro(),
        home=os.path.expanduser("~"),
        program=os.path.dirname(sys.argv[0])
    )
except FileNotFoundError:
    program_exit(1, "설정 파일을 찾을 수 없습니다.", Color.RED)
except NotImplementedError as os_name:
    program_exit(1, f"{os_name}는 지원되는 OS가 아닙니다.", Color.RED)
except Exception:
    program_exit(1, "프로그램 초기화중 오류가 발생했습니다.", Color.RED)

__MAPPING: list[datatype.ShellCommand] = [
    {
        "Argu": True,
        "Command": ("ie",),
        "Exec": edk2.install
    },
    {
        "Argu": True,
        "Command": ("qe",),
        "Exec": qemu.install
    },
    {
        "Argu": False,
        "Command": ("help",),
        "Exec": show_message,
    },
    {
        "Argu": False,
        "Command":("clear", "cls"),
        "Exec": color_print.clear_screen,
    },
    {
        "Argu": False,
        "Command": ("exit", "e"),
        "Exec": program_exit
    },
    {
        "Argu": False,
        "Command": ("color",),
        "Exec": color_print.config.toogle_color_mode
    }
]

__COMMANDS = (
    "ie    : edk2 설치\n"
    "qe    : qemu 설치\n"
    "-------------------------\n"
    "help  : 명령어 목록 보기\n"
    "clear : 화면 초기화\n"
    "color : 컬러 출력 끄기/켜기\n"
    "exit  : 프로그램 나가기"
)

def main():
    processing_config(contexts.config)
    color_print.clear_screen()
    color_print.write("Auto-Setup에 오신 것을 환영합니다!", Color.MAGENTA)
    show_message()

    while True:
        _input = color_print.read("메뉴 입력 > ")
        if not _input:
            continue

        for mapping in __MAPPING:
            if _input in mapping["Command"]:
                if mapping["Argu"]:
                    check_error(mapping["Exec"](contexts))
                else:
                    mapping["Exec"]()
                break
        else:
            color_print.write("없는 기능을 지정했습니다..", Color.RED)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        color_print.clear_screen()
        program_exit(130)
