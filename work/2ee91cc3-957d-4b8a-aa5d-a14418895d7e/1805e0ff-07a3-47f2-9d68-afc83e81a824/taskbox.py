tasks: list[dict] = []  # 唯一的存储：内存 list

def add_task(title: str) -> None:
    if not title.strip():
        raise ValueError("任务标题不能为空")
    tasks.append({"id": len(tasks) + 1, "title": title.strip(), "done": False})

def mark_done(task_id: int) -> dict:
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = True
            return task
    raise ValueError(f"没有 id={task_id} 的任务")

def show_tasks(filter_: str = "all") -> list[str]:
    if filter_ not in {"all", "done", "todo"}:
        raise ValueError(f"不支持的筛选条件：{filter_}")
    picked = [t for t in tasks if filter_ == "all" or t["done"] == (filter_ == "done")]
    return [f"[{'x' if t['done'] else ' '}] #{t['id']} {t['title']}" for t in picked]

if __name__ == "__main__":
    add_task("读懂模块 0 / 1 的资料")
    add_task("写 taskbox.py 并跑通")
    mark_done(1)
    print("\n".join(show_tasks()))
