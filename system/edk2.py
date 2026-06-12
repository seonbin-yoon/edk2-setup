import datetime
import os

from python_data.edk2 import all_func, all_shell
from system import execute
from utils import check, color_print, datatype
from utils.color_print import Color


def install(program_context: datatype.Contexts) -> bool:
    start_time = datetime.datetime.now()
    try:
        _wake(program_context.config)
    except (FileExistsError, NotImplementedError) as error_message:
        color_print.write(error_message, Color.RED)
        return False

    color_print.write("이 작업은 시간이 조금 걸릴 수 있습니다..", Color.MAGENTA)

    func_tasks = _get_func_task_lists()
    shell_tasks = _get_shell_task_lists(program_context.distro)

    _processing_tasks(shell_tasks, program_context)

    task_contexts = datatype.TaskContexts(
        func_task_num=len(func_tasks),
        shell_task_num=len(shell_tasks),
        total_num=len(shell_tasks) + len(func_tasks)
    )

    try:
        execute.shell_run(shell_tasks, task_contexts)
        execute.func_run(func_tasks, task_contexts, program_context)
    except RuntimeError as error_message:
        color_print.write(error_message, Color.RED)
        return False

    color_print.write("")
    end_time = datetime.datetime.now()
    spend_time = end_time - start_time
    color_print.write(f"걸린 시간: {spend_time.seconds // 60}분", Color.YELLOW)
    return True

def _wake(config: datatype.Config):
    color_print.clear_screen()
    color_print.write("edk2 셋팅을 시작합니다..", Color.YELLOW)

    color_print.write("\r미설치 여부 검사 -> ...", Color.YELLOW, end="")
    if os.path.exists(config["edk2_path"]):
        raise FileExistsError(
            "\r설치 여부 검사 -> 실패\n" \
            "이미 edk2 폴더가 존재하므로 더 이상 진행할 수 없습니다."
            )
    color_print.write("\r미설치 여부 검사 -> 통과", Color.GREEN)

    color_print.write("docker 컨테이너 여부 검사 -> ...", Color.BLUE)
    try:
        __check_is_docker()
    except NotImplementedError as error:
        _input = color_print.read("현재 프로그램이 실행중인 곳이 " \
        "docker 컨테이너 내부가 아닌 것 같습니다.\n" \
        "전역에 설치를 할 경우 패키지 꼬임, " \
        "삭제 번거로움 등의 문제가 발생할 수 있습니다.\n" \
        "그래도 괜찮으시다면 y를 입력해주세요.\n"
        "여기에 입력 > ", Color.RED)
        if _input != "y":
            color_print.write("취소합니다.", Color.YELLOW)
            raise NotImplementedError from error

    color_print.write("\r설정 파일 내용 검사 -> ...", Color.YELLOW, end="")
    try:
        check.edk2_config(config)
    except NotImplementedError as error_message:
        raise NotImplementedError(error_message) from error_message
    color_print.write("\r설정 파일 내용 검사 -> 통과", Color.GREEN)

def __check_is_docker():
    if os.path.exists('/.dockerenv'):
        return

    try:
        with open('/proc/1/cgroup') as proc_file:
            if "docker" in proc_file.read():
                return
    except FileNotFoundError:
        pass

    raise NotImplementedError

def _get_shell_task_lists(distro: str) -> list[datatype.Task]:
    if distro == "RHEL":
        from python_data.edk2.RHEL import rhel_command
        task = rhel_command.install_tasks
        task.extend(all_shell.c_install_tasks)
    elif distro == "DEBIAN":
        raise NotImplementedError
    else:
        raise NotImplementedError

    return task

def _get_func_task_lists() -> list[datatype.Function]:
    return all_func.install_tasks

def _processing_tasks(
        raw_tasks: list[datatype.Task],
        program_context: datatype.Contexts):

    for task in raw_tasks:
        if "!Home" in task["Path"]:
            task["Path"] = task["Path"].replace("!Home", program_context.home)
        if "!Edkpath" in task["Path"]:
            task["Path"] = task["Path"].replace(
                "!Edkpath", program_context.config["edk2_path"]
                )

        for num, _exec in enumerate(task["Exec"]):
            if "!Edkpath" in _exec:
                _exec = _exec.replace("!Edkpath", program_context.config["edk2_path"])
                task["Exec"][num] = _exec
