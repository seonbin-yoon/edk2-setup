import os

from python_data.qemu import all_func, all_shell
from system import execute
from utils import check, color_print, datatype
from utils._except import QemuExcept, RunExcept, SettingError
from utils.color_print import Color


def install(program_context: datatype.Contexts) -> bool:
    try:
        _wake(program_context.config)
    except (
        SettingError.InvalidSettingError,
        QemuExcept.QemuExistsError,
        RunExcept.SudoError) as error_message:

        color_print.write(error_message, Color.RED)
        return False

    shell_tasks = _get_shell_tasks(program_context)
    func_tasks = all_func.install_tasks

    execute.processing_tasks(shell_tasks, program_context)

    task_contexts = datatype.TaskContexts(
        shell_task_num=len(shell_tasks),
        func_task_num=len(func_tasks),
        total_num=len(shell_tasks) + len(func_tasks)
    )

    try:
        execute.shell_run(shell_tasks, task_contexts)
        execute.func_run(func_tasks, task_contexts, program_context)
    except RunExcept.FailedRunError as error_message:
        color_print.write(error_message, Color.RED)
        return False

    return True

def _wake(config: datatype.Config):
    color_print.clear_screen()
    color_print.write("qemu 셋팅을 시작합니다..", Color.YELLOW)

    color_print.write("\r미설치 여부 검사 -> ...", Color.YELLOW, end="")
    if os.path.exists(config["qemu_path"]):
        raise QemuExcept.QemuExistsError("\r설치 여부 검사 -> 실패\n" \
            "이미 qemu 폴더가 존재하므로 더 이상 진행할 수 없습니다.")
    color_print.write("\r미설치 여부 검사 -> 통과", Color.GREEN)

    color_print.write("\r설정 파일 내용 검사 -> ...", Color.YELLOW, end="")
    try:
        check.qemu_config(config)
    except SettingError.InvalidSettingError as error_message:
        raise SettingError.InvalidSettingError("\r설정 파일 내용 검사 -> 실패\n" \
        f"{error_message}") from error_message
    color_print.write("\r설정 파일 내용 검사 -> 통과", Color.GREEN)

    color_print.write("시작하기에 앞서, sudo 인증이 필요합니다.", Color.YELLOW)
    try:
        execute.require_sudo()
    except RunExcept.SudoError as error_message:
        raise RunExcept.SudoError(error_message) from error_message
    color_print.write("sudo 인증 성공", Color.GREEN)

def _get_shell_tasks(program_context: datatype.Contexts) -> list[datatype.ShellTask]:
    if program_context.distro == "RHEL":
        from python_data.qemu.RHEL import rhel
        task = rhel.install_tasks
    elif program_context.distro == "DEBIAN":
        from python_data.qemu.DEBIAN import debian
        task = debian.install_tasks
    else:
        raise NotImplementedError

    task.extend(all_shell.install_task)
    return task
