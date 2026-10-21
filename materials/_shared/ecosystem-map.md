# 后端生态"选库地图"

> 后端开发的一大能力是：**遇到一个任务，知道该用哪类工具、有哪些主流选项、如何取舍。**
> 这份地图帮你建立心智索引。遇到新任务时，先定位"这属于哪一类"，再让 AI 在该类里推荐并比较。

## 如何用这份地图

1. 把任务归类（下表的"任务类型"）。
2. 看该类的主流选项与适用场景。
3. 让 AI 针对你的具体约束，在候选里**对比推荐**，并说明理由。
4. 用 [AI 协作检查清单](./ai-collaboration-checklist.md) 核验它推荐的库是否真实、维护活跃、依赖合理。

## 选库地图

| 任务类型 | 主流选项 | 适用 / 取舍 |
|---|---|---|
| Web 框架 | **FastAPI** / Flask / Django | FastAPI：现代、异步、自带校验与文档（本课默认）。Flask：轻量灵活。Django：大而全、自带 ORM/admin。 |
| 数据校验/建模 | **Pydantic v2** / dataclasses / attrs | 对外接口数据校验首选 Pydantic；纯内部数据结构用 dataclass 即可。 |
| ORM / 数据库访问 | **SQLAlchemy 2.x** / SQLModel / Tortoise / 原生 SQL | SQLAlchemy 功能最全；SQLModel 结合 Pydantic 更简洁；简单场景直接写 SQL 也行。 |
| 数据库迁移 | **Alembic** | 配合 SQLAlchemy，管理表结构版本。 |
| HTTP 客户端 | **httpx** / requests | httpx 支持异步；requests 老牌同步。 |
| 异步任务/队列 | **Celery** / RQ / APScheduler / arq | 重任务用 Celery/RQ；定时任务用 APScheduler。 |
| 缓存 | **Redis**（redis-py） | 缓存、会话、简单队列。 |
| 测试 | **pytest** / unittest | pytest 生态最强（fixture、参数化、插件）。 |
| 代码质量 | **ruff**（lint+format）/ **mypy**（类型） / black | ruff 一个工具搞定 lint+格式化，极快。 |
| 包/环境管理 | **uv** / pip + venv / poetry | uv 快且现代（本课默认）；poetry 功能全。 |
| 配置管理 | **pydantic-settings** / python-dotenv | 从环境变量/.env 读配置。 |
| 认证/安全 | **passlib[bcrypt]** / **python-jose** 或 PyJWT | 密码哈希 + JWT 签发校验。 |
| 日志 | 标准库 **logging** / structlog / loguru | 生产建议结构化日志。 |
| 序列化/数据处理 | 标准库 **json** / orjson / pandas | 大数据分析才上 pandas。 |
| 部署 | **Docker** / gunicorn+uvicorn | 容器化 + ASGI 服务器。 |

## 标准库里常被忽视的好东西

遇事先想"标准库有没有"，很多时候不用装第三方：

- `pathlib` — 路径操作（别再用字符串拼路径）
- `datetime` / `zoneinfo` — 时间与时区
- `json` — JSON 读写
- `logging` — 日志
- `dataclasses` — 轻量数据结构
- `enum` — 枚举常量
- `functools` — `lru_cache`、`partial`、`wraps`
- `itertools` / `collections` — 高效迭代与容器（`defaultdict`、`Counter`）
- `typing` — 类型注解
- `secrets` — 生成安全随机 token（别用 `random` 做安全相关）
- `subprocess` — 调外部命令（注意注入风险）

## 评估一个第三方库的快速标准

- 维护是否活跃（最近有提交/发布）？
- Star / 下载量 / 社区规模如何？
- 文档是否清晰？
- 依赖是否沉重、是否和现有栈冲突？
- 是否过度设计——标准库能不能解决？
