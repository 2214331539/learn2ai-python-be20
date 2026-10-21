# 模块 10 · 打包与部署

> 统一结构：概念心智模型 → 最小可运行示例 → 常见坑 → 和 AI 这样协作 → 本周任务

## 概念心智模型

- **可复现**：部署环境必须和开发环境一致。靠锁文件（`uv.lock`）钉死每个依赖的确切版本，避免"我这能跑、线上挂了"。
- **容器（Docker）**：把应用代码 + 依赖 + 运行环境打包成一个可移植镜像，到哪都一样跑。镜像是不可变的交付单元。
- **配置与代码分离（12-factor）**：数据库地址、密钥、运行模式等用**环境变量**在运行时注入，绝不写死在代码或镜像里。同一镜像用不同环境变量即可跑在开发/生产。
- **ASGI 服务器**：FastAPI 自己不是服务器。开发用 `uvicorn --reload`；生产用 uvicorn（或 gunicorn 管理多个 uvicorn worker）托管。
- **可观测性**：生产要有日志（能收集）、健康检查端点（让平台知道服务活没活）。

## 最小可运行示例

```python
# app/core/config.py —— 用 pydantic-settings 从环境变量/.env 读配置
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    secret_key: str                      # 必填，没有就启动失败（好事）
    database_url: str = "sqlite:///./tasks.db"
    debug: bool = False

settings = Settings()  # type: ignore[call-arg]
```

```bash
# .env.example —— 提交这个“示例”，真实 .env 加进 .gitignore 不提交
SECRET_KEY=change-me-to-a-long-random-string
DATABASE_URL=postgresql://user:pass@db:5432/tasks
DEBUG=false
```

```dockerfile
# Dockerfile —— 多阶段精简 + 非 root 运行
FROM python:3.11-slim AS base
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app

# 先只拷依赖清单，利用构建缓存
COPY pyproject.toml uv.lock ./
RUN pip install --no-cache-dir uv && uv sync --frozen --no-dev

COPY app ./app

# 不以 root 运行，缩小被攻破后的影响面
RUN useradd -m appuser
USER appuser

EXPOSE 8000
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```python
# 健康检查端点
@app.get("/healthz")
def healthz():
    return {"status": "ok"}
```

本地运行：`docker build -t tasks . && docker run -p 8000:8000 --env-file .env tasks`

## 常见坑

- **把 `.env` / 密钥打进镜像或提交进仓库**：最常见也最危险。密钥靠运行时环境变量注入，`.env` 必须在 `.gitignore` 里。
- **镜像臃肿**：用完整 `python` 基础镜像、不清缓存、不用 `.dockerignore`——镜像几个 GB。用 `slim` + `--no-cache` + 多阶段。
- **以 root 运行容器**：被攻破后影响面更大。建非 root 用户运行。
- **开发配置上生产**：`debug=True`、SQLite、`--reload` 直接上线——性能差、泄露信息、不稳定。
- **没有健康检查 / 日志收集**：平台无法判断服务死活，出问题无从排查。

## 和 AI 这样协作

- 让 AI 写 Dockerfile 后，审查四点：**有没有把密钥/`.env` 打进镜像？镜像是否精简（slim/多阶段/.dockerignore）？是否非 root 运行？有没有健康检查？**
- 让 AI **逐条解释每个 Docker 指令的作用**，不要照抄——尤其 `COPY` 进去了什么要心里有数（别把密钥、本地数据库文件带进去）。
- 提交前用 `git status` / 搜索确认仓库里没有任何真实密钥或 `.env`。

## 本周任务

1. 贯穿项目 S7：用 pydantic-settings 管理配置，写 Dockerfile 容器化，部署到任一云平台（或本地容器运行并演示）。
2. 提供 `.env.example`；确认真实 `.env` 和任何密钥都不在仓库里。
3. 加 `/healthz` 健康检查端点。
4. 附协作记录，重点说明你对 Dockerfile 的安全/精简审查（见 [检查清单](../_shared/ai-collaboration-checklist.md)）。
