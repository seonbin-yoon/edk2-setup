import datetime
import os

from command_modules.qemu import all_func, all_shell
from modules import check, console, datatype
from modules._except import QemuExcept, RunExcept, SettingError
from modules.console import Color
from modules.functions import get_spend_time
from modules.system import check_need_sudo
from system import execute


def install(program_context: datatype.Contexts) -> bool:
    console.clear_screen()
    console.write("qemu 셋팅을 시작합니다..", Color.YELLOW)
    start_time = datetime.datetime.now()

    try:
        _check_qemu_exists(program_context.config)
        _check_conf(program_context.config)
        need_sudo = check_need_sudo()
        if need_sudo:
            _get_sudo()
    except (
            QemuExcept.QemuExistsError,
            SettingError.InvalidSettingError,
            RunExcept.SudoError
            ) as error:

        console.write(error, Color.RED)
        return False

    shell_tasks = _get_shell_tasks(program_context)
    func_tasks = all_func.install_tasks

    execute.env_var_substitution(shell_tasks, need_sudo, program_context)

    task_contexts = datatype.TaskContexts(
        shell_task_num=len(shell_tasks),
        func_task_num=len(func_tasks),
        total_num=len(shell_tasks) + len(func_tasks)
    )

    try:
        execute.shell_run(shell_tasks, task_contexts)
        execute.func_run(func_tasks, task_contexts, program_context)
    except RunExcept.FailedRunError as error:
        console.write(error, Color.RED)
        return False

    end_time = datetime.datetime.now()
    console.write("")
    spend_time = get_spend_time(start_time, end_time)
    console.write(f"걸린 시간: {spend_time}")
    return True

def _check_qemu_exists(config: datatype.Config):
    console.write("\r미설치 여부 검사 -> ...", Color.YELLOW, end="")
    if os.path.exists(config["qemu_path"]):
        raise QemuExcept.QemuExistsError(
            "\r설치 여부 검사 -> 실패\n" \
            "이미 qemu 폴더가 존재하므로 더 이상 진행할 수 없습니다."
            )
    console.write("\r미설치 여부 검사 -> 통과", Color.GREEN)

def _check_conf(config: datatype.Config):
    console.write("\r설정 파일 내용 검사 -> ...", Color.YELLOW, end="")
    try:
        check.qemu_config(config)
    except SettingError.InvalidSettingError as error:
        raise SettingError.InvalidSettingError(error) from error
    console.write("\r설정 파일 내용 검사 -> 통과", Color.GREEN)

def _get_sudo():
    console.write("시작하기에 앞서, sudo 인증이 필요합니다.", Color.YELLOW)
    try:
        execute.require_sudo()
    except RunExcept.SudoError as error:
        raise RunExcept.SudoError(error) from error
    console.write("sudo 인증 성공", Color.GREEN)

def _get_shell_tasks(program_context: datatype.Contexts) -> list[datatype.ShellTask]:
    if program_context.distro == "RHEL":
        from command_modules.qemu.RHEL import rhel
        task = rhel.install_tasks
    elif program_context.distro == "DEBIAN":
        from command_modules.qemu.DEBIAN import debian
        task = debian.install_tasks
    else:
        raise NotImplementedError

    task.extend(all_shell.install_task)
    return task
