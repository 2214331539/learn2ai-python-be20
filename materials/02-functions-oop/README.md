# 模块 2 · 函数式与面向对象

> 统一结构：概念心智模型 → 最小可运行示例 → 常见坑 → 和 AI 这样协作 → 本周任务

## 概念心智模型

- **一等函数**：在 Python 里函数和整数、字符串一样是"值"——能赋给变量、作为参数传递、作为返回值。这是装饰器、回调、路由注册的基础。
- **装饰器**：本质就是"接收一个函数、返回一个增强后函数"的函数。后端框架里到处是它（`@app.get(...)`、鉴权、缓存）。看懂装饰器，你就不会把框架当黑魔法。
- **类与面向对象**：用类把"数据 + 操作数据的行为"捆在一起。但 Python 不强制 OOP——能用函数清晰表达的，就别硬套类。
- **`dataclass`**：当你只是想要"一个装数据的对象"时，`@dataclass` 自动帮你生成 `__init__`、`__repr__`、`__eq__`，省掉大量样板。
- **类型注解**：`def f(x: int) -> str`。它不在运行时强制校验，但让代码自文档化，也让 mypy、IDE 和 AI 更准确理解你的意图——在 AI 协作里尤其重要。
- **组合优于继承**：需要复用行为时，优先"把另一个对象作为成员持有"，而不是层层继承。

## 最小可运行示例

```python
from dataclasses import dataclass, field
from datetime import datetime
import functools
import time


# 1. dataclass：几行定义一个数据类，自动有 __init__/__repr__/__eq__
@dataclass
class Task:
    title: str
    done: bool = False
    tags: list[str] = field(default_factory=list)  # 可变默认值要用 default_factory！
    created_at: datetime = field(default_factory=datetime.now)


# 2. 装饰器：用 functools.wraps 保留原函数元信息
def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"[{func.__name__}] 耗时 {elapsed:.4f}s")
        return result
    return wrapper


# 3. 一等函数：把函数当参数传
def apply_twice(fn, value):
    return fn(fn(value))


@timer
def slow_square(n: int) -> int:
    time.sleep(0.1)
    return n * n


if __name__ == "__main__":
    t = Task(title="写作业", tags=["python"])
    print(t)                       # dataclass 自动生成可读的 repr
    print(slow_square(5))          # 装饰器打印耗时
    print(apply_twice(lambda x: x + 1, 10))  # 12
```

## 常见坑

- **装饰器丢失原函数信息**：不加 `functools.wraps`，被装饰函数的 `__name__`、docstring 会变成 wrapper 的，调试和框架内省时出问题。
- **dataclass 里的可变默认值**：`tags: list = []` 会在所有实例间共享同一个列表！必须用 `field(default_factory=list)`。
- **过度继承**：一碰到复用就加父类，继承层级越堆越深、越难维护。优先组合。
- **把一切塞进一个巨型类（God Object）**：一个类几百行、什么都管，难测难改。按职责拆分。
- **误以为类型注解会在运行时拦截错误**：它不会。注解是给静态工具和人看的；运行时校验要靠 Pydantic（模块 5）。

## 和 AI 这样协作

本周重点：**让 AI 重构，由你当裁判。**

- 让 AI 把你模块 1 的脚本重构为"函数 + dataclass + 类型注解"的版本，然后你判断：**是更清晰了，还是只是更啰嗦、过度设计了？** 能说出理由才算过关。
- 让 AI 写一个装饰器，并要求它逐步解释"调用时各步按什么顺序执行"。
- 故意让 AI 写一个带"可变默认值坑"的 dataclass，看你能否一眼指出并修正。

## 本周任务

1. 用 `@dataclass` + 完整类型注解重写贯穿项目的 `Task`（和 `Bookmark`）数据结构，正确处理可变默认值。
2. 写一个有实际用途的装饰器（如记录调用、计时），并用 `functools.wraps`。
3. 至少做一次"AI 重构 + 你评判"的练习，在协作记录里写明你接受/否决了哪些改动及理由。
4. 附协作记录（见 [检查清单](../_shared/ai-collaboration-checklist.md)）。
