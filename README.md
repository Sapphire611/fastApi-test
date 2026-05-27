# FastAPI + Supabase

FastAPI 后端，数据库层使用 Supabase（PostgreSQL + REST API）。

## 项目结构

```
app/
├── core/
│   ├── config.py       # 配置（Supabase 连接、密码加密 salt）
│   ├── crypto.py       # SHA-256 密码预哈希（与前端一致）
│   └── database.py     # Supabase 客户端单例
├── api/v1/
│   ├── router.py       # 路由注册
│   ├── health.py       # GET /health
│   └── users.py        # 用户 CRUD + 登录
├── schemas/
│   ├── health.py
│   └── user.py         # UserCreate/Update/Response/Login
├── models/
│   └── user.py         # User 模型（包裹 Supabase 行数据）
├── services/
│   └── user_service.py # 用户业务逻辑
└── main.py
migrations/
└── users.sql            # 数据库建表 DDL
scripts/
├── check_password.py    # 密码格式诊断
└── migrate_password.py  # 密码格式迁移
```

## 快速开始

1. 创建虚拟环境并安装依赖：

   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   .\venv\Scripts\activate    # Windows
   pip install -r requirements.txt
   ```

2. 配置 `.env`（参考 `.env.example`）：

   ```env
   SUPABASE_URL=https://your-project.supabase.co
   SUPABASE_KEY=your-service-role-key
   PASSWORD_SALT=your-salt-must-match-frontend
   ```

3. 启动：

   ```bash
   uvicorn app.main:app --reload
   ```

4. 打开 Swagger UI：http://localhost:8000/docs

## API 端点

| 方法 | 路径 | 说明 |
|------|------|------|
| `POST` | `/api/v1/users/register` | 注册 |
| `POST` | `/api/v1/users/login` | 登录（支持邮箱或用户名） |
| `GET` | `/api/v1/users/` | 用户列表 |
| `GET` | `/api/v1/users/{id}` | 用户详情 |
| `PUT` | `/api/v1/users/{id}` | 更新用户 |
| `DELETE` | `/api/v1/users/{id}` | 删除用户 |
| `GET` | `/api/v1/health` | 健康检查 |

## 密码加密

与 INFP-CMS 前端一致的双重加密：

```
前端: SHA-256(password + PASSWORD_SALT) → 64位 hex
后端: bcrypt(SHA-256 hex) → 存入数据库
```

`PASSWORD_SALT` 必须与前端 `NEXT_PUBLIC_PASSWORD_SALT` 保持一致。
