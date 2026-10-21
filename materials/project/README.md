# 贯穿项目：个人任务/书签 API 服务

> 全课围绕这**一个**项目滚动开发。每个模块给它加一层能力，结课时你手里有一个完整、可部署、带测试的作品集项目。

## 项目简介

做一个"个人任务 & 书签"后端服务：用户可以注册登录，创建/查看/修改/删除自己的任务（task）和书签（bookmark），并能按标签筛选。

选它的原因：需求人人都懂、能自然地覆盖后端所有核心主题（CRUD、认证、权限、数据库、异步、测试、部署），又不至于太庞大。

## 分阶段演进（跟随模块推进）

| 阶段 | 对应模块 | 项目长成什么样 |
|---|---|---|
| S0 | 0–1 | 一个本地单文件脚本，用内存里的 list 存任务，命令行跑。 |
| S1 | 4 | 第一个 FastAPI 服务，`GET/POST /tasks`，数据先存内存。 |
| S2 | 5 | 用 Pydantic 定义 Task/Bookmark 模型，做输入输出校验。 |
| S3 | 6 | 接入 SQLAlchemy + SQLite，数据真正持久化，完整 CRUD。 |
| S4 | 7 | 把 I/O 密集端点改成 async，接入异步数据库驱动。 |
| S5 | 8 | 加用户注册/登录、JWT 认证、"只能操作自己的数据"的授权。 |
| S6 | 9 | 为关键端点写 pytest 测试，接入 ruff + mypy。 |
| S7 | 10 | Docker 化，用环境变量管理配置，部署到云。 |
| S8 | 11 | 结课：独立添加一个全新功能（例如"任务提醒"或"书签标签统计"）。 |

## 目录约定（建议的最终形态）

```
app/
  main.py            # FastAPI 入口
  models.py          # SQLAlchemy 模型
  schemas.py         # Pydantic 模型
  database.py        # 连接与会话
  routers/
    tasks.py
    bookmarks.py
    auth.py
  core/
    config.py        # pydantic-settings 配置
    security.py      # 密码哈希 / JWT
tests/
  conftest.py
  test_tasks.py
Dockerfile
pyproject.toml
.env.example         # 示例配置（不含真实密钥）
```

> 注意：学生自己的项目成果写在 `work/<你的用户UUID>/<作业UUID>/` 下，**不要**写进 `materials/`。这里的骨架仅作参考蓝本。

## 和 AI 这样协作

- 每个阶段开始前，先自己画出"这一阶段要加什么、数据怎么流动"，再让 AI 实现。
- 让 AI 改代码时，一次只改一层，改完立刻运行验证，别一次性重写整个项目。
- 用 [AI 协作检查清单](../_shared/ai-collaboration-checklist.md) 核验每一次产出。
