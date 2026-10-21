# 模块 6 · 数据持久化

> 统一结构：概念心智模型 → 最小可运行示例 → 常见坑 → 和 AI 这样协作 → 本周任务

## 概念心智模型

- **持久化 = 数据重启不丢**：内存数据服务一重启就没了，真实服务要存进数据库。开发用 SQLite（零配置、一个文件），生产常用 PostgreSQL。
- **SQL 基础要懂**：表（table）、行（row）、列（column）、主键（唯一标识一行）、外键（指向另一张表）、增删改查（INSERT/SELECT/UPDATE/DELETE）。
- **ORM 是便利，不是魔法**：SQLAlchemy 让你用 Python 对象操作表、少写 SQL；但你必须**能看懂它生成的 SQL**，否则会写出低效查询。
- **会话（session）与事务**：对数据库的一组操作在一个会话里进行；事务保证"要么全成功、要么全回滚"。用完要正确提交/关闭。
- **迁移（Alembic）**：表结构会演进（加字段、改类型），用迁移做版本化管理，绝不手改生产库。

## 最小可运行示例

```python
# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

engine = create_engine("sqlite:///./tasks.db", echo=False)  # echo=True 可打印真实 SQL
SessionLocal = sessionmaker(bind=engine, autoflush=False)

class Base(DeclarativeBase):
    pass
```

```python
# app/models.py  —— SQLAlchemy 2.x 风格
from datetime import datetime, timezone
from sqlalchemy import String, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from .database import Base

class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    done: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )
```

```python
# app/main.py 片段：依赖注入会话 + 参数化查询（防注入）
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from .database import SessionLocal, engine, Base
from .models import Task
from .schemas import TaskCreate, TaskOut

Base.metadata.create_all(engine)  # 教学演示用；生产用 Alembic 迁移
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db          # 请求结束后在 finally 里关闭，避免连接泄漏
    finally:
        db.close()

@app.post("/tasks", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate, db: Session = Depends(get_db)):
    task = Task(title=payload.title)
    db.add(task)
    db.commit()           # 事务提交，数据真正落库
    db.refresh(task)      # 取回数据库生成的 id/created_at
    return task

@app.get("/tasks/{task_id}", response_model=TaskOut)
def get_task(task_id: int, db: Session = Depends(get_db)):
    # 用 ORM 参数化查询，绝不用字符串拼 SQL
    task = db.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="任务不存在")
    return task
```

## 常见坑

- **SQL 注入**：用 f-string / `+` 把用户输入拼进 SQL（`f"SELECT * FROM t WHERE name='{name}'"`）——极危险。始终用 ORM 或参数化查询。
- **N+1 查询**：拿到一批任务后，循环里再逐条查每个任务的标签——1 次变 N+1 次查询。用 `join` / `selectinload` 一次查出。
- **会话未关闭/未提交**：忘了 `commit()` 数据不落库；忘了 `close()` 连接泄漏。用依赖注入 + `finally` 统一管理。
- **直接改生产库结构**：手动 `ALTER TABLE` 改线上库——不可复现、易出事。走 Alembic。
- **把创建表 `create_all` 当迁移用**：它只建不改，字段一变就失效。教学可用，生产必须迁移。

## 和 AI 这样协作

- 让 AI 写 CRUD 后，带着三个问题审查：**有没有字符串拼 SQL？有没有 N+1？会话是否正确提交并关闭？**
- 打开 `echo=True`，让数据库**打印出 AI 的 ORM 实际生成了什么 SQL**，自己判断效率——这是识破 N+1 的最直接方法。
- 让 AI 生成 Alembic 迁移脚本后，**先读懂它要对表做什么**再执行，尤其是删列/改类型这类不可逆操作。

## 本周任务

1. 贯穿项目 S3：接入 SQLAlchemy + SQLite，把 Task/Bookmark 的 CRUD 全部改为数据库持久化。
2. 用依赖注入管理会话；至少建一次 Alembic 迁移。
3. 开启 `echo=True` 检查生成的 SQL，确认没有 N+1；确认全程无字符串拼 SQL。
4. 附协作记录，重点说明你如何排查注入与 N+1 风险（见 [检查清单](../_shared/ai-collaboration-checklist.md)）。
