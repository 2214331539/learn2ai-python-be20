# 模块 8 · 认证与安全（重点模块）

> 统一结构：概念心智模型 → 最小可运行示例 → 常见坑 → 和 AI 这样协作 → 本周任务
> 本模块是"AI 代码安全审查"训练的核心。后端最常出的严重事故都在这里。

## 概念心智模型

- **认证 vs 授权**：认证（Authentication）= 证明"你是谁"（登录）；授权（Authorization）= 决定"你能做什么"（权限）。两者缺一不可——很多事故是"认证做了、授权忘了"。
- **密码绝不明文存储**：用成熟的慢哈希算法（bcrypt / argon2）+ 自动加盐。数据库泄露时也无法还原密码。
- **JWT（无状态令牌）**：登录成功后签发一个带签名的令牌，客户端之后每次请求带上它；服务端用密钥验证签名即可确认身份，无需在服务端存会话。
- **纵深防御**：输入校验、参数化查询、最小权限、密钥隔离、不泄露内部错误——层层设防，不指望单点。
- **密钥属于配置，不属于代码**：JWT secret、数据库密码从环境变量读，绝不写进代码提交到仓库。

## 最小可运行示例

```python
# app/core/security.py
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
import jwt  # PyJWT
from .config import settings  # SECRET_KEY 等从环境变量读（见模块 10）

pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(raw: str) -> str:
    return pwd.hash(raw)                 # 自动加盐

def verify_password(raw: str, hashed: str) -> bool:
    return pwd.verify(raw, hashed)

def create_token(user_id: int) -> str:
    payload = {
        "sub": str(user_id),
        "exp": datetime.now(timezone.utc) + timedelta(hours=1),
    }
    return jwt.encode(payload, settings.secret_key, algorithm="HS256")

def decode_token(token: str) -> int:
    data = jwt.decode(token, settings.secret_key, algorithms=["HS256"])
    return int(data["sub"])
```

```python
# app/routers/tasks.py 片段：认证 + 授权（关键在授权！）
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

router = APIRouter()
bearer = HTTPBearer()

def current_user_id(cred: HTTPAuthorizationCredentials = Depends(bearer)) -> int:
    try:
        return decode_token(cred.credentials)
    except Exception:
        # 不要把内部异常细节返回给客户端
        raise HTTPException(status_code=401, detail="无效或过期的令牌")

@router.get("/tasks/{task_id}")
def get_task(task_id: int, uid: int = Depends(current_user_id),
             db: Session = Depends(get_db)):
    task = db.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="任务不存在")
    # 授权检查：这条数据到底是不是他的？少了这一行就是越权漏洞（IDOR）
    if task.owner_id != uid:
        raise HTTPException(status_code=403, detail="无权访问")
    return task
```

## 常见坑（后端高频严重漏洞，务必记牢）

- **越权 / IDOR**：只校验了"登录了没"，却没校验"这条数据是不是他的"。把 `task_id` 换成别人的就能读/改别人数据。**每个访问具体资源的端点都要做归属校验。**
- **SQL 注入**：字符串拼 SQL（见模块 6）。
- **密码处理错误**：明文存储、用 md5/sha1（快哈希，易被暴力破解）、不加盐。必须用 bcrypt/argon2。
- **密钥硬编码**：`SECRET_KEY = "mysecret"` 写进代码提交到 Git——相当于把钥匙贴在门上。
- **敏感信息进日志**：日志打印密码、完整 token、信用卡号。
- **错误信息泄露**：把 Python 栈追踪、SQL 语句直接返回给客户端，暴露内部结构。
- **JWT 无过期时间 / 不校验过期**：令牌永久有效，泄露即长期沦陷。

## 和 AI 这样协作（本模块核心训练）

- **安全审查训练**：课堂会给一段"能跑但有坑"的 AI 风格认证代码，你要逐条找出所有安全问题并修复。练的就是"看起来对"和"真的安全"之间的鉴别力。
- AI 实现认证后，逐条对照 [检查清单的安全红线](../_shared/ai-collaboration-checklist.md)：注入、越权、密码、密钥、日志、错误泄露。
- **特别警惕授权缺失**：AI 很容易只做认证、漏掉"这条数据是不是你的"的归属校验。每个资源端点都要主动追问这一点。
- 牢记红线：**密钥、权限边界、认证逻辑，AI 只能给建议，必须由你亲自审查把关。**

## 本周任务

1. 贯穿项目 S5：加用户注册/登录（密码 bcrypt 哈希）、JWT 认证、以及"用户只能操作自己数据"的授权。
2. `SECRET_KEY` 等从环境变量读取，仓库中不得出现任何真实密钥。
3. 完成一次 AI 代码安全审查练习，列出你发现并修复的每个问题。
4. 附协作记录，重点写安全审查过程（见 [检查清单](../_shared/ai-collaboration-checklist.md)）。
