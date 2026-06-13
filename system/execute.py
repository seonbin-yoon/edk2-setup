import subprocess

from utils import color_print, datatype
from utils._except import RunExcept
from utils.color_print import Color


def shell_run(
        shell_tasks: list[datatype.ShellTask],
        task_contents: datatype.TaskContexts):

    for num, task in enumerate(shell_tasks):
        color_print.write(
            f"\r[{num + 1}/{task_contents.total_num}] {task['Message']} -> 진행중..",
            Color.BLUE, end="")
        try:
            subprocess.run(
                task["Exec"],
                cwd=task["Path"],
                capture_output=True,
                text=True,
                check=True
                )
        except subprocess.CalledProcessError as error:
            raise RunExcept.FailedRunError(
                f"\r[{num + 1}/{task_contents.total_num}] "\
                f"{task['Message']} -> 실패.{"":<5}\n"\
                f"{error}") from error
        color_print.write(
            f"\r[{num + 1}/{task_contents.total_num}] "\
            f"{task['Message']} -> 완료.{"":<5}",
            Color.GREEN)

def func_run(
    func_tasks: list[datatype.FunctionTask],
    task_contents: datatype.TaskContexts,
    program_context: datatype.Contexts):

    for num, func_task in enumerate(func_tasks):
        func = func_task["Func"]
        color_print.write(
            f"\r[{(task_contents.shell_task_num + num) + 1}/"\
            f"{task_contents.total_num}] "\
            f"{func_task['Message']} -> 진행중..",
            Color.BLUE, end="")
        try:
            func(program_context)
        except (FileNotFoundError, PermissionError) as error:
            raise RunExcept.FailedRunError(
                f"\r[{(task_contents.shell_task_num + num) + 1}/"\
                f"{task_contents.total_num}] "\
                f"{func_task['Message']} -> 실패.{"":<5}\n"
                f"{error}") from error
        color_print.write(
            f"\r[{(task_contents.shell_task_num + num) + 1}/"\
            f"{task_contents.total_num}] "\
            f"{func_task['Message']} -> 완료.{"":<5}",
            Color.GREEN)
