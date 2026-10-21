# 课程资料总索引 · Python 后端开发（AI 辅助）

> 本课的核心理念：**在 AI 时代，这门课教的不是背语法，而是让你建立足够扎实的心智模型，从而能"指挥、读懂、验证、调试" AI 写出来的后端代码。**

课程由两条交织主线组成：

- **主线 A（理解）**：Python 语言特性 + 后端生态地图
- **主线 B（产出）**：在 AI 协作下，把需求做成一个能跑、能测、能部署的后端服务

## 课程目标

1. 读得懂 Python 代码，能判断 AI 给的代码"对不对、好不好、安不安全"。
2. 掌握后端核心概念：HTTP/API、数据持久化、异步、认证、测试、部署。
3. 掌握一套可复现工作流（需求 → 提示 → 生成 → 验证 → 迭代），借助 AI 快速完成真实后端任务。
4. 熟悉主流生态工具，知道"什么任务该用什么库"。

## 贯穿项目

全程围绕一个真实项目滚动开发：**一个"个人任务/书签 API 服务"**，从单文件脚本逐步长成带数据库、认证、测试、容器化部署的 FastAPI 服务。见 [`project/`](./project/README.md)。

## 模块地图

| 模块 | 主题 | 目录 |
|---|---|---|
| 0 | 环境与工作流 | [`00-setup/`](./00-setup/README.md) |
| 1 | Python 语言精要 | [`01-language/`](./01-language/README.md) |
| 2 | 函数式与面向对象 | [`02-functions-oop/`](./02-functions-oop/README.md) |
| 3 | 标准库与生态地图 | [`03-stdlib-ecosystem/`](./03-stdlib-ecosystem/README.md) |
| 4 | HTTP 与第一个 API | [`04-http-api/`](./04-http-api/README.md) |
| 5 | 数据校验与建模 | [`05-validation/`](./05-validation/README.md) |
| 6 | 数据持久化 | [`06-persistence/`](./06-persistence/README.md) |
| 7 | 异步编程 | [`07-async/`](./07-async/README.md) |
| 8 | 认证与安全 | [`08-auth-security/`](./08-auth-security/README.md) |
| 9 | 测试与质量 | [`09-testing/`](./09-testing/README.md) |
| 10 | 打包与部署 | [`10-deploy/`](./10-deploy/README.md) |
| 11 | 综合项目周 | [`11-capstone/`](./11-capstone/README.md) |

## 贯穿性共享资料（反复使用）

- [`_shared/ai-collaboration-checklist.md`](./_shared/ai-collaboration-checklist.md) — **AI 协作检查清单**（每份作业都要用）
- [`_shared/ecosystem-map.md`](./_shared/ecosystem-map.md) — 后端生态"选库地图"
- [`_shared/glossary.md`](./_shared/glossary.md) — 术语表

## 多模态资料（不只 Markdown）

课程资料提供多种表现形式，互为补充：

- **🏠 课程主页（HTML）**：[`index.html`](./index.html) — 可视化总入口，嵌入路线图、模块导航卡片、资源链接。**建议在浏览器中打开。**
- **📄 PDF 讲义**：[`_shared/ai-collaboration-checklist.pdf`](./_shared/ai-collaboration-checklist.pdf) — AI 协作检查清单的可打印速查卡，适合随身/发给学生。
- **🌐 交互速查页（HTML）**：
  - [`_shared/ai-checklist-card.html`](./_shared/ai-checklist-card.html) — AI 协作清单网页版（PDF 的源）
  - [`_shared/http-reference.html`](./_shared/http-reference.html) — HTTP 方法与状态码速查
- **🖼 图解（SVG，矢量可缩放）**，位于 [`_shared/assets/`](./_shared/assets/)，已嵌入对应讲义，每个模块至少一张：
  - `course-roadmap.svg` — 课程路线图（主页）
  - `env-isolation.svg` — 虚拟环境隔离（模块 0）
  - `names-and-objects.svg` — 变量是标签/可变 vs 不可变（模块 1）
  - `decorator.svg` — 装饰器工作原理（模块 2）
  - `choose-library.svg` — 选库决策流程（模块 3）
  - `http-lifecycle.svg` — HTTP 请求生命周期（模块 4）
  - `validation-gate.svg` — Pydantic 校验门（模块 5）
  - `n-plus-1.svg` — ORM 的 N+1 查询坑（模块 6）
  - `sync-vs-async.svg` — 同步 vs 异步（模块 7）
  - `auth-flow.svg` — 认证与授权流程（模块 8）
  - `testing.svg` — 测试金字塔 + 识破假通过（模块 9）
  - `deploy-pipeline.svg` — 打包与部署流水线（模块 10）
  - `backend-architecture.svg` — 后端分层架构（项目说明）
  - `project-evolution.svg` — 项目演进 S0→S8（项目说明）

> 阅读建议：浏览器开 `index.html` 纵览全局与速查，编辑器/仓库里读 Markdown 讲义深入细节，PDF 打印随身。

## 每份讲义的统一结构

> 概念心智模型 → 最小可运行示例 → 常见坑 → "和 AI 这样协作" → 本周任务

## 技术选型（本课默认）

- Python 3.11+、包管理 `uv`（兼容 pip/venv）
- Web 框架 FastAPI + Pydantic v2
- ORM：SQLAlchemy 2.x；数据库：开发用 SQLite，部署示例用 PostgreSQL
- 测试：pytest；质量：ruff + mypy
- 部署：Docker + 任一容器平台

> 选型会随生态更新，但课程强调的是"概念"而非特定库，换框架时迁移成本很低。
