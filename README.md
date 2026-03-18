# FastAPI Scaffold

## Setup

1. Create a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   .\venv\Scripts\activate   # Windows
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```

## 🎯 快速测试

1. 启动服务器：
   source venv/bin/activate
   uvicorn app.main:app --reload

2. 打开浏览器访问：
    - Swagger UI: http://localhost:8000/docs
    - ReDoc: http://localhost:8000/redoc

### 📝 Swagger 功能

- 📖 查看所有 API 端点
- 🧪 直接测试 API 接口
- 📋 查看请求/响应模型
- 🔐 配置认证 (如果有)
- 📊 查看详细的参数说明
