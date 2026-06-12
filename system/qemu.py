import os

from python_data.qemu import all_func
from system import execute
from utils import check, color_print, datatype
from utils.color_print import Color


def install(program_context: datatype.Contexts) -> bool:
    try:
        _wake(program_context.config)
    except (NotImplementedError, FileExistsError) as error_message:
        color_print.write(error_message, Color.RED)
        return False

    func_task = all_func.install_tasks
    task_contexts = datatype.TaskContexts(
        len(func_task),
        0,
        len(func_task)
    )
    try:
        execute.func_run(func_task, task_contexts, program_context)
    except RuntimeError as error_message:
        color_print.write(error_message, Color.RED)
        return False

    return True

def _wake(config: datatype.Config):
    color_print.clear_screen()
    color_print.write("qemu 셋팅을 시작합니다..", Color.YELLOW)

    color_print.write("\r미설치 여부 검사 -> ...", Color.YELLOW, end="")
    if os.path.exists(config["qemu_path"]):
        raise FileExistsError("\r설치 여부 검사 -> 실패\n" \
            "이미 qemu 폴더가 존재하므로 더 이상 진행할 수 없습니다.")
    color_print.write("\r미설치 여부 검사 -> 통과", Color.GREEN)

    color_print.write("\r설정 파일 내용 검사 -> ...", Color.YELLOW, end="")
    try:
        check.qemu_config(config)
    except NotImplementedError as error_message:
        raise NotImplementedError("\r설정 파일 내용 검사 -> 실패\n" \
        f"{error_message}") from error_message
    color_print.write("\r설정 파일 내용 검사 -> 통과", Color.GREEN)
