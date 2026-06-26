from include import check_list as check_list
from modules import datatype
from modules._except import SettingError


def edk2_config(config: datatype.Config):
    error_list: list[str] = []

    for basic_check in check_list.EDK_BASIC_CHECKS:
        if not config[basic_check["Check"]]:
            error_list.append(basic_check["Message"] + "\n")

    for extra_check in check_list.EDK_EXTRA_CHECKS:
        if config[extra_check["Depends_on"]] and extra_check["Function"]():
            error_list.append(extra_check["Message"] + "\n")

    if error_list:
        raise SettingError.InvalidSettingError("".join(error_list))

def qemu_config(config: datatype.Config):
    if len(config["qemu_path"].split("/")) < 3:
        raise SettingError.InvalidSettingError(
            "root 바로 밑에 qemu 폴더를 생성할 수 없습니다.")
