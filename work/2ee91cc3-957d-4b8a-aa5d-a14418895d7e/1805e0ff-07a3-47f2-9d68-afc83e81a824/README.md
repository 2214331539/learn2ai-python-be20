# 作业一 · 搭好环境，跑通第一个脚本

贯穿项目“个人任务 / 书签 API 服务”的 S0 版本：一个用内存 `list` 存任务的命令行小脚本。

## 1. 环境

| 工具 | 版本 | 检查命令 |
|---|---|---|
| Python | 3.11.5 | `py -3.11 --version` |
| uv | 0.13.5 | `uv --version` |
| Git | 2.56.0.windows.2 | `git --version` |

说明：本机 `python` 命令被 Windows 应用执行别名占用，直接运行会提示 “Python was not found”，所以统一用 `py -3.11` 调用已安装的 Python 3.11.5，或用 `uv` 创建并进入独立虚拟环境。虚拟环境目录 `.venv/` 已被 `.gitignore` 排除。

## 2. 目录结构

```
.
├── .gitignore
├── README.md
├── hello.py
└── taskbox.py
```

本目录位于课程仓库的 `work/<用户UUID>/<作业UUID>/` 下，由课程仓库统一做 Git 版本管理（提交与分享由课程应用完成），因此没有在这里再嵌套执行 `git init`：嵌套仓库会被父仓库当作嵌入式仓库，反而破坏成果提交。`.gitignore` 仍然负责排除虚拟环境、`__pycache__` 和 `.env`。

## 3. 如何运行

```bash
# 方式一：使用系统 Python 3.11
py -3.11 hello.py
py -3.11 taskbox.py

# 方式二：用 uv 建独立虚拟环境后运行
uv venv --python 3.11 .venv
uv run --no-project python hello.py
uv run --no-project python taskbox.py
```

> 若把输出重定向到文件或管道，可加 `-X utf8`（如 `py -3.11 -X utf8 hello.py`），避免 Windows 默认 GBK 编码造成中文乱码。

## 4. 运行输出

```text
$ py -3.11 hello.py
Python 版本：3.11.5
你好，Python 后端开发！环境已就绪。

$ py -3.11 taskbox.py
[x] #1 读懂模块 0 / 1 的资料
[ ] #2 写 taskbox.py 并跑通
```

`[x]` 表示已完成，`[ ]` 表示未完成。

## 5. taskbox.py 说明（共 25 行）

- `add_task(title)`：添加任务；标题为空或全是空格时抛 `ValueError`。
- `mark_done(task_id)`：把指定 id 的任务标记为完成；找不到时抛 `ValueError`。
- `show_tasks(filter_="all")`：列出任务，支持 `all` / `done` / `todo` 三种筛选。
- 语言要点：`show_tasks` 用了**列表推导式**筛选和格式化；三个函数都是**自定义函数**；三处输入校验都用了**异常处理**（`raise ValueError` 配合调用方 `try/except` 使用的 EAFP 风格）。
- 存储：模块级 `tasks` 列表模拟数据库，进程结束后数据清空——这是 S0 的设计边界，后续阶段会接入真正的持久化。

## 6. 验证记录

| 验证项 | 结果 |
|---|---|
| `hello.py` 正常输出 Python 版本与自定义一行 | 通过 |
| `taskbox.py` 添加 2 个任务并完成第 1 个 | 通过 |
| 添加空标题 / 全空格标题 | 抛 `ValueError`，符合预期 |
| 完成不存在的任务 id | 抛 `ValueError`，符合预期 |
| 非法筛选条件 | 抛 `ValueError`，符合预期 |
| `all` / `done` / `todo` 三种筛选 | 均返回正确结果 |
| 连续多轮添加、清空、再添加 | 未出现数据串扰 |
| 函数签名中的可变默认参数 | 不存在（详见协作记录第 4 条） |

## 7. AI 协作记录

1. **我让 AI 做了什么**：按作业要求起草 `.gitignore`、`hello.py`，以及一个 15–25 行、用内存 `list` 存任务的 `taskbox.py`，明确要求包含推导式、异常处理、自定义函数，并且不能出现可变默认参数。
2. **我改了 / 否决了什么**：初版 `hello.py` 第二行用了 ✅，实际在 Windows 的 GBK 管道输出下抛 `UnicodeEncodeError`，我删掉 emoji、改成纯中文；AI 曾建议在成果目录内再 `git init`，我否决了——该目录已属于课程仓库，嵌套 `.git` 会被当成嵌入式仓库，影响应用的提交与分享；`taskbox.py` 中保留 `filter_: str = "all"` 作为唯一默认参数（字符串不可变）。
3. **我做了哪些验证**：分别用 `py -3.11` 和 `uv run` 跑通 `hello.py`；运行 `taskbox.py` 得到“已完成 / 未完成”两行输出；用临时校验脚本测试空标题、未知任务 id、非法筛选条件都会抛 `ValueError`，并测了 `all` / `done` / `todo` 三种筛选与连续多轮使用。
4. **如何确认没有可变默认参数坑**：用 `inspect.signature` 检查三个函数的默认值，只有 `filter_: str = "all"` 是不可变字符串，没有 `[]`、`{}` 这类默认容器；任务列表是模块级显式状态，函数内通过 `tasks.append(...)` 修改，而不是把列表放进参数默认值；实际签名为 `(title: str) -> None`、`(task_id: int) -> dict`、`(filter_: str = 'all') -> list[str]`。
