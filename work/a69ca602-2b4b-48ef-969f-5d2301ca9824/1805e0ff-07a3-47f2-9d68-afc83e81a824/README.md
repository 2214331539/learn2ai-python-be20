# 作业一 · 搭好环境，跑通第一个脚本

本目录是贯穿项目“个人任务/书签 API 服务”的 S0 雏形：一个用内存列表保存任务的命令行脚本，以及环境检查脚本。

## 运行环境

- 操作系统：Windows + PowerShell
- Python：3.13.2（项目独立虚拟环境 `.venv`）
- 包管理：uv 0.11.7
- 版本控制：Git 2.48.1.windows.1

项目用 `pyproject.toml` 声明 `requires-python = ">=3.11"`，没有第三方运行依赖。`uv venv --python 3.13` 创建了独立环境，`.venv/` 已被 `.gitignore` 排除。

## 文件结构

```text
1805e0ff-07a3-47f2-9d68-afc83e81a824/
├── .gitignore        # 排除虚拟环境、缓存、.env 等
├── README.md         # 运行说明、输出与协作记录
├── hello.py          # 打印 Python 版本和一行自定义内容
├── pyproject.toml    # 最小项目元数据
├── taskbox.py        # S0 任务清单（25 行）
└── uv.lock           # uv 生成的锁定文件（无第三方依赖）
```

## 如何运行

在 PowerShell 中进入本目录后执行：

```powershell
uv venv --python 3.13
uv run python hello.py
uv run python taskbox.py
```

`taskbox.py` 是交互式脚本，支持以下命令：

| 命令 | 作用 |
|---|---|
| `add <任务内容>` | 添加一条未完成任务 |
| `列表` 或 `list` | 按编号列出全部任务及完成状态 |
| `done <编号>` | 把指定编号的任务标成完成 |
| `quit` | 退出，退出后内存任务清空（S0 阶段不持久化） |

## 运行结果

### hello.py

```text
$ uv run python hello.py
Python 版本：3.13.2
你好，后端开发！今天也要写出能解释清楚的代码。
```

### taskbox.py

```text
$ uv run python taskbox.py
taskbox> list
暂无任务
taskbox> add 完成作业一
taskbox> add 复习 Python 推导式
taskbox> list
1. [ ] 完成作业一
2. [ ] 复习 Python 推导式
taskbox> done 1
已完成：完成作业一
taskbox> done 99
错误：没有编号为 99 的任务
taskbox> done 0
错误：没有编号为 0 的任务
taskbox> done abc
错误：编号必须是整数
taskbox> list
1. [x] 完成作业一
2. [ ] 复习 Python 推导式
taskbox> add
错误：请输入 add <任务> / 列表 / done <编号> / quit
taskbox> quit
```

`add` 成功时不额外打印确认，随后用 `列表` 可以看到新任务；这样输出更短，也便于确认列表中真实存在。

## 关键实现与验证

- 任务保存在模块级 `tasks` 列表中；`add`、`mark`、`show` 是三个自定义函数。
- `show` 用列表推导式一次生成带编号和勾选状态的显示行。
- `mark` 用 `try/except (IndexError, TypeError)` 处理不存在的编号；调用层用 `except ValueError` 处理 `done abc` 这类非整数输入。
- 显式检查 `number < 1`，避免 `done 0` 使用 Python 的负索引误伤最后一条任务。
- 已执行 `uv run python -m py_compile hello.py taskbox.py`，语法检查通过。
- 已用 AST 遍历 `taskbox.py` 的全部函数：`add`、`mark`、`show` 的默认参数数量均为 0，`mutable_defaults` 检查结果为空列表。
- 已用 `git check-ignore -v` 确认 `.venv/`、`__pycache__/` 和 `.env` 分别被 `.gitignore` 第 7、2、12 行匹配。

## Git 管理说明

课程仓库根目录本身已经执行过 `git init`，本成果位于该仓库的 `work/<用户UUID>/<作业UUID>/` 中，因此直接复用课程仓库的版本控制，不在成果目录里再嵌套一个 `.git`，以免外层 Git 把子目录当成嵌入仓库而漏交文件。提交与推送由课程应用用已连接的 GitHub 身份完成。

## AI 协作记录

我让 AI 按题目约束起草 `hello.py`、`taskbox.py` 和 `.gitignore`，并要求 `taskbox.py` 不超过 25 行、用内存 `list` 实现添加/列出/标记完成。AI 最初给出的是每次运行只执行一条 `sys.argv` 命令的版本，我否决了它，因为进程退出后内存就丢失，`add` 之后再 `list` 根本看不到任务，于是改成同一个交互式会话内循环读取命令。我还把标完成的索引校验改成显式的 `number < 1` 报错，因为只靠 `tasks[number - 1]` 的 `IndexError` 时，`done 0` 会取到 Python 的最后一个元素，误标最后一条任务。我实际用 uv 虚拟环境跑了 `hello.py`，并在 `taskbox.py` 中测试空列表、添加、列出、完成，以及 `done 99`、`done 0`、`done abc`、空 `add` 和未知命令。关于可变默认参数，我用 AST 遍历了所有函数定义，确认三个函数的默认参数数量都是 0，因此没有共享 `list`/`dict`/`set` 默认值的风险，而不是只靠肉眼扫一遍。
