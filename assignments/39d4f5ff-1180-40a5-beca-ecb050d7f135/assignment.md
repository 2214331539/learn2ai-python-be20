---
id: 39d4f5ff-1180-40a5-beca-ecb050d7f135
title: 作业十一 · 打包与部署（S7）
---

# 作业十一 · 打包与部署（S7）

对应 [模块 10 · 打包与部署](../../materials/10-deploy/README.md)，项目阶段 **S7**。

把服务从"我电脑上能跑"变成"到哪都能跑"——容器化，并把配置与代码分离。

## 你要做的事

1. 用 **pydantic-settings** 从环境变量/`.env` 读取配置（`SECRET_KEY`、`DATABASE_URL`、`DEBUG`）。
2. 写一个 **Dockerfile**：精简（slim / 多阶段 / `.dockerignore`）、**非 root 运行**。
3. 提供 **`.env.example`**；确认真实 `.env` 和任何密钥都不在仓库里（加入 `.gitignore`）。
4. 加 **`/healthz`** 健康检查端点。
5. 本地用容器运行并访问成功（或部署到任一云平台），记录过程。

## 提交内容

放在 `work/<你的用户UUID>/39d4f5ff-1180-40a5-beca-ecb050d7f135/`：

- `Dockerfile`、`.dockerignore`、`.env.example`、配置代码、`README.md`（运行/部署记录）；
- AI 协作记录。

> 成果由应用用你的 GitHub 身份提交并请求分享确认，你不需要自己 `git push`。

## AI 协作记录（必写）

见 [AI 协作检查清单](../../materials/_shared/ai-collaboration-checklist.md)。特别说明：你对 AI 写的 Dockerfile 做了哪些安全/精简审查（密钥是否被打进镜像？是否非 root？镜像是否过大？）。

## 评分标准（100 分）

- 配置外置（pydantic-settings）正确（20 分）
- Dockerfile 精简、非 root、可构建运行（30 分）
- 仓库无真实密钥、`.env.example` 到位（20 分）
- 健康检查端点 + 运行/部署记录（15 分）
- AI 协作记录真实具体（15 分）

## 提示

- 把密钥或 `.env` 打进镜像/提交进仓库，是最常见也最危险的错误。
- 同一个镜像应能靠不同环境变量跑在开发与生产——这就是"配置与代码分离"。
