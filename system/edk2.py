import datetime
import os

from command_modules.edk2 import all_func, all_shell
from modules import check, console, datatype
from modules._except import Edk2Except, RunExcept, SettingError
from modules.console import Color
from modules.functions import get_spend_time
from modules.system import check_need_sudo
from system import execute


def install(program_context: datatype.Contexts) -> bool:
    console.clear_screen()
    console.write("edk2 셋팅을 시작합니다..", Color.YELLOW)
    start_time = datetime.datetime.now()

    try:
        _check_edk2_exists(program_context.config)
        _check_is_docker()
        _check_conf(program_context.config)
        need_sudo = check_need_sudo()
        if need_sudo:
            _get_sudo()
    except (
            Edk2Except.Edk2ExistsError,
            Edk2Except.NotDockerError,
            SettingError.InvalidSettingError,
            RunExcept.SudoError
            ) as error:

        if isinstance(error, Edk2Except.NotDockerError):
            try:
                _handling_docker_error()
            except RunExcept.CancelError:
                return False

        console.write(error, Color.RED)
        return False

    console.write("이 작업은 시간이 조금 걸릴 수 있습니다..", Color.MAGENTA)

    func_tasks = _get_func_task_lists()
    shell_tasks = _get_shell_task_lists(program_context.distro)

    execute.env_var_substitution(shell_tasks, need_sudo, program_context)

    task_contexts = datatype.TaskContexts(
        func_task_num=len(func_tasks),
        shell_task_num=len(shell_tasks),
        total_num=len(shell_tasks) + len(func_tasks)
    )

    try:
        execute.shell_run(shell_tasks, task_contexts)
        execute.func_run(func_tasks, task_contexts, program_context)
    except RunExcept.FailedRunError as error:
        console.write(error, Color.RED)
        return False

    console.write("")
    end_time = datetime.datetime.now()
    spend_time = get_spend_time(start_time, end_time)
    console.write(f"걸린 시간: {spend_time}", Color.YELLOW)
    return True

def _check_edk2_exists(config: datatype.Config):
    console.write("\r미설치 여부 검사 -> ...", Color.YELLOW, end="")
    if os.path.exists(config["edk2_path"]):
        raise Edk2Except.Edk2ExistsError(
            "\r설치 여부 검사 -> 실패\n" \
            "이미 edk2 폴더가 존재하므로 더 이상 진행할 수 없습니다."
            )
    console.write("\r미설치 여부 검사 -> 통과", Color.GREEN)

def _check_is_docker():
    console.write("docker 컨테이너 여부 검사..", Color.BLUE)

    if os.path.exists('/.dockerenv'):
        return

    try:
        with open('/proc/1/cgroup') as proc_file:
            if "docker" in proc_file.read():
                return
    except FileNotFoundError:
        pass

    raise Edk2Except.NotDockerError

def _check_conf(config: datatype.Config):
    console.write("\r설정 파일 내용 검사 -> ...", Color.YELLOW, end="")
    try:
        check.edk2_config(config)
    except SettingError.InvalidSettingError as error:
        raise SettingError.InvalidSettingError(error) from error
    console.write("\r설정 파일 내용 검사 -> 통과", Color.GREEN)

def _handling_docker_error():
    _input = console.read(
    "현재 프로그램이 실행중인 곳이 " \
    "docker 컨테이너 내부가 아닌 것 같습니다.\n" \
    "전역에 설치를 할 경우 패키지 꼬임, " \
    "삭제 번거로움 등의 문제가 발생할 수 있습니다.\n" \
    "그래도 괜찮으시다면 y를 입력해주세요.\n"
    "여기에 입력 > ", Color.RED)
    if _input != "y":
        console.write("취소합니다.", Color.YELLOW)
        raise RunExcept.CancelError

def _get_sudo():
    console.write("시작하기에 앞서, sudo 인증이 필요합니다.", Color.YELLOW)
    try:
        execute.require_sudo()
    except RunExcept.SudoError as error:
        raise RunExcept.SudoError(error) from error
    console.write("sudo 인증 성공", Color.GREEN)

def _get_shell_task_lists(distro: str) -> list[datatype.ShellTask]:
    if distro == "RHEL":
        from command_modules.edk2.RHEL import rhel
        task = rhel.install_tasks
    elif distro == "DEBIAN":
        from command_modules.edk2.DEBIAN import debian
        task = debian.install_tasks
    else:
        raise NotImplementedError

    task.extend(all_shell.install_tasks)
    return task

def _get_func_task_lists() -> list[datatype.FunctionTask]:
    return all_func.install_tasks
