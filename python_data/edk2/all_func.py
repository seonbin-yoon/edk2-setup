import os
import shutil
import uuid

from utils import datatype


def _add_bashrc_func(context: datatype.Contexts):
    function = __processing_bash_func(context)
    bashrc_path = os.path.join(context.home, ".bashrc")

    with open(bashrc_path, "a", encoding='utf-8') as bashrc:
        bashrc.writelines(function)

def __processing_bash_func(context: datatype.Contexts) -> list[str]:
    source_file_path = os.path.join(context.program, "data", "bash.txt")
    function: list[str] = []

    with open(source_file_path, encoding='utf-8') as source_file:
        for line in source_file:
            if "!Edk2path" in line:
                line = line.replace("!Edk2path", context.config['edk2_path'])

            function.append(line)

    return function

def _config_target_txt(context: datatype.Contexts):
    conf_path = os.path.join(
        context.config["edk2_path"],
        "edk2",
        "Conf",
        "target.txt"
        )

    with open(conf_path, encoding='utf-8') as target_file:
        new_target_file: list[str] = []

        for line in target_file:
            if not line:
                continue

            if not line.startswith("#"):
                if "ACTIVE_PLATFORM" in line:
                    line = f"  ACTIVE_PLATFORM = {context.config['active_platform']}\n"
                elif "TOOL_CHAIN_TAG" in line:
                    line = f"  TOOL_CHAIN_TAG = {context.config['tool_chain_tag']}\n"
                elif "TARGET_ARCH" in line:
                    line = f"  TARGET_ARCH = {context.config['target_arch']}\n"
                elif "MAX_CONCURRENT_THREAD_NUMBER" in line:
                    line = "  MAX_CONCURRENT_THREAD_NUMBER = "\
                    f"{context.config['max_concurrent_thread_number']}\n"

            new_target_file.append(f"{line}")

    with open(conf_path, "w", encoding='utf-8') as target_file:
        target_file.writelines(new_target_file)

def _make_project_folder(context: datatype.Contexts):
    project_folder_path = os.path.join(
            context.config["edk2_path"],
            "edk2",
            "MdeModulePkg",
            "Application",
            context.config["project_name"]
        )
    os.makedirs(project_folder_path)

def _set_project_folder(context: datatype.Contexts):
    __copy_inf_file(context)

    inf_path = os.path.join(
        context.config["edk2_path"],
        "edk2",
        "MdeModulePkg",
        "Application",
        f"{context.config["project_name"]}",
        f"{context.config["project_name"]}.inf"
    )

    new_inf_file: list[str] = []
    passing: bool = False

    with open(inf_path, encoding='utf-8') as inf_file:
        for line in inf_file:
            if not line or passing:
                continue

            if not line.startswith("#"):
                if "BASE_NAME" in line:
                    line = "  BASE_NAME                      " \
                    f"= {context.config['loader_name']}\n"
                elif "FILE_GUID" in line:
                    line = "  FILE_GUID                      "\
                    f"= {str(uuid.uuid4()).upper()}\n"
                elif "VERSION_STRING" in line:
                    line = "  VERSION_STRING                 "\
                    f"= {context.config['version']}\n"
                elif "ENTRY_POINT" in line:
                    line = "  ENTRY_POINT                    " \
                    f"= {context.config["function_in"]}\n"
                elif "UEFI_HII_RESOURCE_SECTION" in line:
                    line = "  UEFI_HII_RESOURCE_SECTION      " \
                    "= FALSE\n"
                elif "MODULE_UNI_FILE" in line:
                    new_inf_file.append("")
                    continue
                elif "[FeaturePcd]" in line:
                    new_inf_file.append("")
                    passing = True
                    continue

            new_inf_file.append(f"{line}")

    with open(inf_path, "w", encoding='utf-8') as inf_file:
        inf_file.writelines(new_inf_file)

def __copy_inf_file(context: datatype.Contexts):
    source_path = os.path.join(
            context.config["edk2_path"],
            "edk2",
            "MdeModulePkg",
            "Application",
            "HelloWorld",
            "HelloWorld.inf"
        )
    target_path = os.path.join(
        context.config["edk2_path"],
        "edk2",
        "MdeModulePkg",
        "Application",
        f"{context.config["project_name"]}",
        f"{context.config["project_name"]}.inf"
    )

    shutil.copy(source_path, target_path)


def _config_mde_module_dsc(context: datatype.Contexts):
    dsc_path = os.path.join(
        context.config['edk2_path'],
        "edk2",
        "MdeModulePkg",
        "MdeModulePkg.dsc"
        )
    new_dsc_file: list[str] = []

    with open(dsc_path, encoding='utf-8') as dsc_file:
        for line in dsc_file:
            if not line:
                continue

            if not line.startswith("#"):
                if "[Components]" in line:
                    project_dsc_file = os.path.join(
                        "MdeModulePkg",
                        "Application",
                        context.config["project_name"],
                        f"{context.config["project_name"]}.inf"
                    )
                    line = f"{line}"\
                    f"  {project_dsc_file}\n"

            new_dsc_file.append(line)

    with open(dsc_path, "w", encoding='utf-8') as dsc_file:
        dsc_file.writelines(new_dsc_file)

install_tasks: list[datatype.Function] = [
    {
        "Message": "bashrc 환경 활성화 함수 추가",
        "Func": _add_bashrc_func
    },
    {
        "Message": "전역 정보 수정 (target.txt)",
        "Func": _config_target_txt
    },
    {
        "Message": "프로젝트 폴더 생성",
        "Func": _make_project_folder
    },
    {
        "Message": "프로젝트 폴더 설정 (.inf)",
        "Func": _set_project_folder
    },
    {
        "Message": "MdeModulePkg.dsc에 프로젝트 등록",
        "Func": _config_mde_module_dsc
    }
]
