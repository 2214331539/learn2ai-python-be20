# 模块 4 · HTTP 与第一个 API

> 统一结构：概念心智模型 → 最小可运行示例 → 常见坑 → 和 AI 这样协作 → 本周任务

## 概念心智模型

- **HTTP 是请求-响应**：客户端发一个请求（**方法** + **路径** + **头** + **体**），服务器返回一个响应（**状态码** + **头** + **体**）。就这么简单。
- **方法有语义**：GET 取数据（只读、幂等）、POST 新建、PUT/PATCH 修改、DELETE 删除。别用 GET 去改数据。
- **状态码会说话**：2xx 成功（200 OK、201 Created）、4xx 客户端错（400 请求错、401 未认证、403 越权、404 找不到、422 校验失败）、5xx 服务端错（500）。
- **REST 风格**：以"资源"（如 task）为中心，用 URL 定位资源、用方法表达操作：`GET /tasks`（列表）、`POST /tasks`（新建）、`GET /tasks/{id}`（单个）。
- **FastAPI 心智**：一个端点 = 一个函数 + 一个装饰器。请求参数通过函数签名声明，FastAPI 自动解析、校验、生成文档。
- **无状态**：HTTP 本身不记得你上次是谁；数据存内存会随重启消失（引出模块 6 的持久化）。

## 最小可运行示例

```python
# app/main.py —— 运行： uv run uvicorn app.main:app --reload
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel  # 模块 5 会深入，这里先用最简形式

app = FastAPI(title="任务服务 S1")

# 先用内存存数据（重启即失，模块 6 换成数据库）
_tasks: list[dict] = []
_next_id = 1


class TaskIn(BaseModel):
    title: str
    done: bool = False


@app.get("/")
def root():
    return {"service": "tasks", "status": "ok"}


@app.get("/tasks")
def list_tasks():
    return _tasks


@app.post("/tasks", status_code=status.HTTP_201_CREATED)  # 创建成功返回 201
def create_task(task: TaskIn):
    global _next_id
    record = {"id": _next_id, **task.model_dump()}
    _tasks.append(record)
    _next_id += 1
    return record


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for t in _tasks:
        if t["id"] == task_id:
            return t
    # 找不到就返回 404，而不是返回 200 + null
    raise HTTPException(status_code=404, detail="任务不存在")
```

启动后打开 `http://127.0.0.1:8000/docs`，FastAPI 自动生成的交互式文档里可以直接点按钮测试每个端点。

## 常见坑

- **用错方法**：用 GET 去创建/修改数据——违反语义，还可能被缓存或预取误触发。
- **永远返回 200**：出错也返回 200 + `{"error": ...}`，客户端无法用状态码判断成败。该 4xx/5xx 就用。
- **把业务逻辑全写在路由函数里**：路由应只负责"收请求、调逻辑、返响应"，复杂逻辑抽到单独模块，便于测试。
- **忘了无状态**：以为内存里的数据会一直在——重启就没了。
- **路径参数类型不声明**：`task_id` 不写 `: int`，拿到的是字符串，比较时对不上。

## 和 AI 这样协作

- 让 AI 从零搭起这个 API 后，**你亲自打开 `/docs` 把每个端点点一遍**，验证行为和状态码是否符合预期——不要只看代码就相信它对。
- 让 AI 解释："一个 `POST /tasks` 请求进来后，数据是怎么一步步流到 `create_task` 函数、又怎么变成响应返回的？"
- 让 AI 帮你设计 REST 路径时，检查它是否符合资源语义（而不是 `/getTask`、`/createTaskNow` 这种）。

## 本周任务

1. 贯穿项目 S1：用 FastAPI 实现 `GET /tasks`、`POST /tasks`、`GET /tasks/{id}`，数据存内存。
2. 正确使用状态码（创建返回 201，找不到返回 404）。
3. 用 `/docs` 把所有端点手动验证一遍，截图或记录结果。
4. 附协作记录（见 [检查清单](../_shared/ai-collaboration-checklist.md)）。
