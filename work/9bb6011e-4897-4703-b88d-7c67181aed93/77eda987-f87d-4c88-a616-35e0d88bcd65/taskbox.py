"""作业二：用推导式和自定义异常扩展内存任务清单。"""


class TaskNotFound(LookupError):
    """任务编号不存在。"""


def add_task(tasks, title):
    title = title.strip()
    if not title:
        raise ValueError("任务标题不能为空")
    task = {"id": len(tasks) + 1, "title": title, "done": False}
    tasks.append(task)
    return task


def find_task(tasks, task_id):
    try:
        return next(task for task in tasks if task["id"] == task_id)
    except StopIteration:
        raise TaskNotFound(f"找不到任务 {task_id}") from None


def complete_task(tasks, task_id):
    task = find_task(tasks, task_id)
    task["done"] = True
    return task


def filter_tasks(tasks, keyword):
    keyword = keyword.strip().casefold()
    return [task for task in tasks if keyword in task["title"].casefold()]


def count_pending(tasks):
    return len([task for task in tasks if not task["done"]])


def format_tasks(tasks):
    rows = [f"{task['id']}. {'[x]' if task['done'] else '[ ]'} {task['title']}" for task in tasks]
    return "\n".join(rows) or "暂无任务"


def taskbox():
    tasks = []
    while True:
        try:
            command = input("命令(add/list/done/filter/count/quit)> ").strip()
            if command == "quit":
                break
            if command == "add":
                task = add_task(tasks, input("任务标题> "))
                print(f"已添加任务 {task['id']}")
            elif command == "list":
                print(format_tasks(tasks))
            elif command == "done":
                task_id = int(input("任务编号> "))
                task = complete_task(tasks, task_id)
                print(f"已完成任务 {task['id']}")
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
    taskbox()
