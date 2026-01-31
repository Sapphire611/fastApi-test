"""
初始化用户数据脚本
运行方式: python scripts/init_users.py
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext
from datetime import datetime
from bson import ObjectId

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# MongoDB 配置
MONGODB_URL = "mongodb://localhost:27017"
DATABASE_NAME = "fastapi_db"

# 初始用户数据
INITIAL_USERS = [
    {
        "_id": ObjectId("6971ada6026f72c98aa1d972"),
        "username": "Admin",
        "email": "admin@test.com",
        "password": "$2b$12$88q8HQEqsv33mXvhGmWLt.fEQivLNg5innUvWlRUj.RYOqek.LFQ.",
        "userType": "admin",
        "isActive": True,
        "createdAt": datetime(2026, 1, 22, 0, 0, 0, 1000),
        "updatedAt": datetime(2026, 1, 22, 6, 27, 11, 84000),
        "__v": 1
    },
    {
        "_id": ObjectId("6971d69b41ae5852d777df6e"),
        "username": "admin2@test.com",
        "email": "806990525@qq.com",
        "password": "$2b$10$kz7DC.IfvK08x8cLqIG/2.IM1Xkksp96bcpOKF4Niz7PgGR6L2uU6",
        "userType": "admin",
        "isActive": True,
        "createdAt": datetime(2026, 1, 22, 7, 49, 47, 945000),
        "updatedAt": datetime(2026, 1, 22, 7, 49, 47, 945000),
        "__v": 0
    }
]


async def init_users():
    """初始化用户数据"""
    # 连接到 MongoDB
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client[DATABASE_NAME]
    users_collection = db.users

    print(f"📦 连接到数据库: {DATABASE_NAME}")

    # 清空现有用户数据（可选）
    choice = input("⚠️  是否清空现有用户数据？(y/N): ").strip().lower()
    if choice == 'y':
        await users_collection.delete_many({})
        print("🗑️  已清空现有用户数据")

    # 插入初始用户数据
    for user in INITIAL_USERS:
        # 检查用户是否已存在
        existing = await users_collection.find_one({"_id": user["_id"]})
        if existing:
            print(f"⏭️  用户 {user['username']} 已存在，跳过")
            continue

        # 插入用户
        await users_collection.insert_one(user)
        print(f"✅ 创建用户: {user['username']} ({user['email']})")

    # 统计用户数量
    count = await users_collection.count_documents({})
    print(f"\n📊 当前数据库中共有 {count} 个用户")

    # 显示所有用户
    print("\n📋 用户列表:")
    async for user in users_collection.find():
        print(f"   - {user['username']} ({user['email']}) - Type: {user['userType']}")

    # 关闭连接
    client.close()
    print("\n✨ 初始化完成！")


async def create_new_user(username: str, email: str, password: str, user_type: str = "user"):
    """创建新用户"""
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client[DATABASE_NAME]
    users_collection = db.users

    # 检查邮箱是否已存在
    existing = await users_collection.find_one({"email": email})
    if existing:
        print(f"❌ 邮箱 {email} 已被注册")
        client.close()
        return

    # 创建用户
    user_doc = {
        "username": username,
        "email": email,
        "password": pwd_context.hash(password),
        "userType": user_type,
        "isActive": True,
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow(),
        "__v": 0
    }

    await users_collection.insert_one(user_doc)
    print(f"✅ 创建用户: {username} ({email})")

    client.close()


if __name__ == "__main__":
    import sys

    print("=" * 50)
    print("🚀 用户数据初始化脚本")
    print("=" * 50)

    if len(sys.argv) > 1 and sys.argv[1] == "create":
        # 创建新用户
        if len(sys.argv) < 4:
            print("用法: python scripts/init_users.py create <用户名> <邮箱> <密码> [类型]")
            print("示例: python scripts/init_users.py create testuser test@example.com 123456 admin")
            sys.exit(1)

        username = sys.argv[2]
        email = sys.argv[3]
        password = sys.argv[4]
        user_type = sys.argv[5] if len(sys.argv) > 5 else "user"

        asyncio.run(create_new_user(username, email, password, user_type))
    else:
        # 初始化默认用户
        asyncio.run(init_users())
