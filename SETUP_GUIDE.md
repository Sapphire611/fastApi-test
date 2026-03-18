# FastAPI PostgreSQL 项目使用指南

## 🚀 快速开始

### Mac/Linux 用户

#### 1. 使用 Makefile (推荐)
```bash
# 查看所有可用命令
make help

# 完整设置：创建虚拟环境 + 安装依赖 + 初始化数据库
make all

# 或者分步骤执行
make venv          # 创建虚拟环境
make install       # 安装依赖
make init-db       # 初始化数据库
make start         # 启动开发服务器

# 运行测试
make test

# 查看如何激活虚拟环境
make activate
```

#### 2. 使用启动脚本
```bash
# 启动开发服务器
./start-dev.sh
```

#### 3. 手动操作
```bash
# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 初始化数据库
python scripts/init_db.py

# 启动服务器
uvicorn app.main:app --reload
```

### Windows 用户

#### 1. 使用 Makefile (推荐)
```bash
# 查看所有可用命令
make help

# 完整设置
make all

# 分步骤执行
make venv
make install
make init-db
make start

# 运行测试
make test

# 查看激活命令
make activate
```

#### 2. 使用启动脚本
```bash
# 启动开发服务器
start-dev.bat
```

#### 3. 手动操作
```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 初始化数据库
python scripts/init_db.py

# 启动服务器
uvicorn app.main:app --reload
```

## 📋 Makefile 命令说明

| 命令 | 说明 |
|------|------|
| `make help` | 显示帮助信息 |
| `make venv` | 创建虚拟环境 |
| `make install` | 安装项目依赖 |
| `make activate` | 显示激活虚拟环境的命令 |
| `make init-db` | 初始化数据库表 |
| `make test` | 运行测试 |
| `make start` | 启动开发服务器 |
| `make clean` | 清理虚拟环境 |
| `make all` | 完整项目设置 |
| `make dev` | 安装依赖、初始化数据库并启动服务器 |

## 🗄️ 数据库设置

### 前置要求
- 已安装 PostgreSQL
- PostgreSQL 服务正在运行

### 创建数据库

#### Mac/Linux
```bash
# 创建开发数据库
createdb -U postgres postgres

# 创建测试数据库
createdb -U postgres fastapi_test_db
```

#### Windows
```bash
# 创建开发数据库
createdb -U postgres postgres

# 创建测试数据库
createdb -U postgres fastapi_test_db
```

### 配置环境变量

复制示例配置文件：
```bash
cp .env.example .env
```

根据需要编辑 `.env` 文件中的数据库配置。

## 🧪 运行测试

```bash
# 激活虚拟环境后
pytest tests/ -v

# 或使用 Makefile
make test
```

## 🛠️ 开发工作流

1. **激活虚拟环境**
   - Mac/Linux: `source venv/bin/activate`
   - Windows: `venv\Scripts\activate`

2. **安装/更新依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **初始化数据库**
   ```bash
   python scripts/init_db.py
   ```

4. **启动开发服务器**
   ```bash
   uvicorn app.main:app --reload
   ```

5. **访问 API 文档**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## 🔧 故障排除

### 虚拟环境问题
```bash
# 清理并重新创建虚拟环境
make clean
make venv
make install
```

### 数据库连接问题
1. 确保 PostgreSQL 正在运行
2. 检查 `.env` 文件中的数据库配置
3. 确保数据库已创建

### 依赖安装问题
```bash
# 升级 pip 后重新安装
pip install --upgrade pip
pip install -r requirements.txt
```

## 📞 获取帮助

- 查看所有可用命令：`make help`
- 查看激活虚拟环境的方法：`make activate`
- 查看 API 文档：http://localhost:8000/docs

## 🎯 主要变更

### MongoDB → PostgreSQL 迁移
- 数据库从 MongoDB 迁移到 PostgreSQL
- 字段命名从 camelCase 改为 snake_case
- ID 从 MongoDB ObjectId 改为 UUID
- 使用 SQLAlchemy async 替代 Motor

### API 字段变更
- `_id` → `id`
- `userType` → `user_type`
- `isActive` → `is_active`
- `createdAt` → `created_at`
- `updatedAt` → `updated_at`
