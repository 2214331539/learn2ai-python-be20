"""作业三：以 dataclass、类型注解和日志装饰器重构任务清单。"""

from collections.abc import Callable
from dataclasses import dataclass, field
from functools import wraps
import logging
from typing import ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")
logger = logging.getLogger(__name__)


@dataclass
class Task:
    id: int
    title: str
    done: bool = False
    tags: list[str] = field(default_factory=list)


class TaskNotFound(LookupError):
    """任务编号不存在。"""


def log_call(function: Callable[P, R]) -> Callable[P, R]:
    """记录操作的开始、成功或失败，不记录任务内容，也不吞掉异常。"""
    @wraps(function)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        logger.info("%s: 开始", function.__name__)
        try:
            result = function(*args, **kwargs)
        except Exception:
            logger.warning("%s: 失败", function.__name__)
            raise
        logger.info("%s: 完成", function.__name__)
        return result

    return wrapper


@log_call
def add_task(tasks: list[Task], title: str, tags: list[str] | None = None) -> Task:
    """添加非空标题的任务，并复制传入的标签。"""
    title = title.strip()
    if not title:
        raise ValueError("任务标题不能为空")
    task = Task(id=len(tasks) + 1, title=title)
    if tags is not None:
        task.tags.extend(tags)
    tasks.append(task)
    return task


def find_task(tasks: list[Task], task_id: int) -> Task:
    try:
        return next(task for task in tasks if task.id == task_id)
    except StopIteration:
        raise TaskNotFound(f"找不到任务 {task_id}") from None


@log_call
def complete_task(tasks: list[Task], task_id: int) -> Task:
    """完成指定任务；重复完成不会影响其他任务。"""
    task = find_task(tasks, task_id)
    task.done = True
    return task


def filter_tasks(tasks: list[Task], keyword: str) -> list[Task]:
    keyword = keyword.strip().casefold()
    return [task for task in tasks if keyword in task.title.casefold()]


def count_pending(tasks: list[Task]) -> int:
    return len([task for task in tasks if not task.done])


def format_tasks(tasks: list[Task]) -> str:
    rows = [f"{task.id}. {'[x]' if task.done else '[ ]'} {task.title}" for task in tasks]
    return "\n".join(rows) or "暂无任务"


def taskbox() -> None:
    tasks: list[Task] = []
    while True:
        try:
            command = input("命令(add/list/done/filter/count/quit)> ").strip()
            if command == "quit":
                break
            if command == "add":
                task = add_task(tasks, input("任务标题> "))
                print(f"已添加任务 {task.id}")
            elif command == "list":
                print(format_tasks(tasks))
            elif command == "done":
                task_id = int(input("任务编号> "))
                task = complete_task(tasks, task_id)
                print(f"已完成任务 {task.id}")
            elif command == "filter":
                print(format_tasks(filter_tasks(tasks, input("关键字> "))))
            elif command == "count":
                print(f"未完成任务：{count_pending(tasks)}")
            else:
                print("未知命令，请使用 add/list/done/filter/count/quit")
        except TaskNotFound as error:
            print(f"操作失败：{error}")
        except ValueError as error:
            print(f"输入错误：{error}")
        except EOFError:
            break


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    taskbox()
