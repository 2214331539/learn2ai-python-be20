# 模块 0 · 环境与工作流

> 统一结构：概念心智模型 → 最小可运行示例 → 常见坑 → 和 AI 这样协作 → 本周任务

## 概念心智模型

写 Python 前，先搞懂三件事，它们是后面一切的地基：

1. **解释器**：Python 代码不是直接给机器跑的，而是交给一个叫"解释器"的程序逐行执行。你电脑上可能有多个 Python 版本，搞清"现在用的是哪个"至关重要。
2. **虚拟环境（venv）**：每个项目应该有自己独立的依赖环境，互不污染。否则项目 A 要 `库==1.0`、项目 B 要 `库==2.0` 就会打架。
3. **项目结构 + Git**：代码放进一个有规矩的目录，并用 Git 记录每一次改动。AI 协作时，清晰的项目结构能让 AI 更准确地理解上下文。

一句话心智模型：**"一个项目 = 一个目录 + 一个独立环境 + 一份版本历史"**。

## 最小可运行示例

本课使用 `uv`（现代、快；也兼容传统 pip/venv 工作流）。

```bash
# 1. 创建项目目录并进入
uv init my-first-backend
cd my-first-backend

# 2. 添加一个依赖（以 fastapi 为例）
uv add fastapi

# 3. 运行一个脚本
uv run python hello.py
```

`hello.py`：

```python
import sys

print(f"Python 版本：{sys.version}")
print("环境就绪 ✅")
```

> 如果你用传统方式：`python -m venv .venv` → 激活 → `pip install fastapi`。原理相同。

## 常见坑

- **用错 Python**：系统自带的 Python 和你装的可能不是同一个。用 `python --version` / `which python`（Windows 用 `where python`）确认。
- **没激活虚拟环境就装包**：包会被装到全局，污染系统。始终确认命令行提示符里有环境标识。
- **把 `.venv` / 密钥 / `__pycache__` 提交进 Git**：一定要配 `.gitignore`。
- **路径带中文或空格**：有些工具会出问题，项目目录尽量用英文、无空格。

## 和 AI 这样协作

- 让 AI 帮你写 `.gitignore`、`pyproject.toml` 时，**要它解释每一行在做什么**，别当黑盒。
- 环境报错（找不到模块、版本冲突）时，把**完整报错 + 你运行的命令 + 操作系统**一起发给 AI，而不是只说"装不上"。
- 让 AI 帮你规划项目目录结构，并说明"为什么这样分层"。

## 本周任务

1. 安装好 Python 3.11+ 与 `uv`，创建本课的贯穿项目目录，初始化 Git。
2. 写一个 `hello.py` 打印 Python 版本，成功运行。
3. 配好 `.gitignore`，完成第一次 commit。
4. 附一段协作记录：你让 AI 帮你做了什么、你验证了什么（见 [检查清单](../_shared/ai-collaboration-checklist.md)）。
