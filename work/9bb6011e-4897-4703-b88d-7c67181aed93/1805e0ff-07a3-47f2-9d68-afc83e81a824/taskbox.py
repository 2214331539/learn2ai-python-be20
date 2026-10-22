def taskbox():
    tasks = []
    while True:
        try:
            command = input("命令(add/list/done/quit)> ").strip()
            if command == "quit": break
            if command == "add":
                title = input("任务标题> ").strip()
                if not title: raise ValueError("任务标题不能为空")
                tasks.append({"title": title, "done": False})
                print(f"已添加任务 {len(tasks)}")
            elif command == "list":
                rows = [f"{i}. {'[x]' if t['done'] else '[ ]'} {t['title']}" for i, t in enumerate(tasks, 1)]
                print("\n".join(rows) or "暂无任务")
            elif command == "done":
                number = int(input("任务编号> "))
                if not 1 <= number <= len(tasks): raise ValueError("任务不存在")
                tasks[number - 1]["done"] = True
                print(f"已完成任务 {number}")
            else:
                print("未知命令，请使用 add/list/done/quit")
        except ValueError as error:
            print(f"输入错误：{error}")
        except EOFError: break
if __name__ == "__main__": taskbox()
