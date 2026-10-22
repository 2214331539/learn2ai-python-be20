# 作业二：Python 语言特性

用途：Learn2ai 团队内测用作业。代码和文字由 Codex 按[作业要求](../../../assignments/77eda987-f87d-4c88-a616-35e0d88bcd65/assignment.md)生成，自动验证由 Codex 执行，学员尚未确认逐行理解。文件仅保存在本地，未由 Codex 上传或提交。

## 文件与运行

需要 Python 3.10 或以上，只使用标准库。在本目录运行：

```sh
python taskbox.py
python bugs.py
python -m unittest -v
```

- [taskbox.py](taskbox.py)：任务清单与自定义异常。
- [bugs.py](bugs.py)：两类错误及修正版。
- [test_taskbox.py](test_taskbox.py)：可重复运行的行为与边界测试。
- [运行记录](运行记录.txt)：本机实际执行结果。
- [AI 协作记录](AI协作记录.md)：工作分工与个人复核状态。
- `.gitignore`：忽略虚拟环境和 Python 缓存。

程序支持 `add` 添加、`list` 列出、`done` 完成、`filter` 筛选、`count` 统计和 `quit` 退出。任务只保存在本次进程的内存中，退出后清空；这是延续作业一的范围。

可依次输入下面的内容（每行一次回车）：

```text
add
学习 Python
add
整理作业
filter
python
count
done
1
count
list
done
0
quit
```

筛选会显示 `1. [ ] 学习 Python`，未完成数量从 2 变为 1，列表显示 `1. [x] 学习 Python` 和 `2. [ ] 整理作业`。编号 0 不存在时提示“操作失败：找不到任务 0”，随后仍可继续输入命令。

## 三行代码的阅读理解

下面三行均来自 `taskbox.py`；解释由 AI 编写，供学员复核。

### 1. 找到首个匹配任务

```python
return next(task for task in tasks if task["id"] == task_id)
```

生成器表达式逐个检查任务编号，`next` 只取第一个匹配对象，不创建完整的中间列表。没有匹配时会抛出 `StopIteration`，`find_task` 将它转换成 `TaskNotFound`；CLI 在调用处捕获并显示可读提示。这是先尝试操作、再处理失败的 EAFP 做法，避免先查是否存在、再查一次取对象。

### 2. 不区分大小写的关键字筛选

```python
return [task for task in tasks if keyword in task["title"].casefold()]
```

列表推导式保留标题包含关键字的任务，返回新的结果列表。前一行已对关键字做 `strip().casefold()`，这里也对标题做 `casefold()`，因此 `python` 能匹配 `Python`，`STRASSE` 能匹配 `Straße`。空关键字匹配全部任务；没有匹配返回空列表。结果中的任务对象仍是原来的字典，筛选不会重新编号。

### 3. 统计未完成数量

```python
return len([task for task in tasks if not task["done"]])
```

推导式先选出 `done` 为假的任务，再取列表长度；空任务列表自然得到 0。这样直接满足本题“使用推导式”的要求；如果数据量很大，可考虑 `sum(1 for ...)` 避免中间列表，本题没有为此扩大范围。

## 改错练习

`bugs.py` 中的坏写法仅供演示，业务脚本没有使用可变集合默认参数。

| 错误 | 为什么错 | 修正与预期结果 |
| --- | --- | --- |
| `append_bad(item, items=[])` | 默认列表在定义函数时创建，不会每次调用都重新创建 | `items=None`，函数内部在 `None` 时创建列表；先后传 A、B，分别得到 `['A']`、`['B']` |
| 用 `left is right` 判断列表内容相等 | `is` 比较对象身份，两份独立但内容相同的列表不是同一对象 | 用 `left == right` 比较内容；例子 `[1, 2]` 与另一个 `[1, 2]` 的结果为 `True` |

`items is None` 是正确的单例判断；修正版显式接收列表时会修改调用者提供的列表，只有省略参数时才新建列表。

## 验证与边界

本机 Python 3.13.15：9 项单元测试通过，并通过独立的命令行流程检查；原始输入和输出见运行记录。覆盖空标题、无效编号、重复完成、Unicode 筛选、空列表、筛选后编号、默认列表隔离和错误输入后继续运行。

编号从 1 开始，当前不提供删除功能；`filter` 返回的列表可以读取原任务对象，不是深拷贝。没有增加文件存储、网络或第三方依赖。Learn2ai 的实际提交、分享和教师评分未在本次执行。
