tasks: list[dict[str, object]] = []

def add(title: str) -> None: tasks.append({"title": title, "done": False})
def mark(number: int) -> str:
    try:
        if number < 1: raise IndexError
        tasks[number - 1]["done"] = True
        return f"已完成：{tasks[number - 1]['title']}"
    except (IndexError, TypeError):
        return f"错误：没有编号为 {number} 的任务"

def show() -> None:
    rows = [f"{i}. [{'x' if task['done'] else ' '}] {task['title']}" for i, task in enumerate(tasks, 1)]
    print("\n".join(rows) if rows else "暂无任务")

for line in iter(lambda: input("taskbox> "), "quit"):
    action, _, value = line.partition(" ")
    if action == "add" and value.strip():
        add(value.strip())
    elif action in ("列表", "list"):
        show()
    elif action == "done":
        try: print(mark(int(value)))
        except ValueError: print("错误：编号必须是整数")
    else: print("错误：请输入 add <任务> / 列表 / done <编号> / quit")
