"""
初始化用户数据脚本 (PostgreSQL)
运行方式: python scripts/init_users.py
"""
import asyncio
import uuid
from passlib.context import CryptContext
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy import select
from app.core.config import settings
from app.models.user import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 创建数据库引擎
engine = create_async_engine(settings.DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# 初始用户数据 (PostgreSQL 格式)
INITIAL_USERS = [
    {
        "id": uuid.UUID("6971ada6-026f-72c9-8aa1-d97200000000"),  # 转换为 UUID
        "username": "Admin",
        "email": "admin@test.com",
        "password": "$2b$12$88q8HQEqsv33mXvhGmWLt.fEQivLNg5innUvWlRUj.RYOqek.LFQ.",
        "user_type": "admin",
        "is_active": True,
        "created_at": datetime(2026, 1, 22, 0, 0, 0, 1000),
        "updated_at": datetime(2026, 1, 22, 6, 27, 11, 84000),
    },
    {
        "id": uuid.UUID("6971d69b-41ae-5852-d777-df6e00000000"),  # 转换为 UUID
        "username": "admin2@test.com",
        "email": "806990525@qq.com",
        "password": "$2b$10$kz7DC.IfvK08x8cLqIG/2.IM1Xkksp96bcpOKF4Niz7PgGR6L2uU6",
        "user_type": "admin",
        "is_active": True,
        "created_at": datetime(2026, 1, 22, 7, 49, 47, 945000),
        "updated_at": datetime(2026, 1, 22, 7, 49, 47, 945000),
    }
]


async def init_users():
    """初始化用户数据"""
    async with AsyncSessionLocal() as session:
        print(f"📦 连接到数据库: {settings.POSTGRES_DB}")

        # 清空现有用户数据（可选）
        choice = input("⚠️  是否清空现有用户数据？(y/N): ").strip().lower()
        if choice == 'y':
            from sqlalchemy import text
            await session.execute(text("TRUNCATE TABLE users CASCADE"))
            await session.commit()
            print("🗑️  已清空现有用户数据")

        # 插入初始用户数据
        for user_data in INITIAL_USERS:
            # 检查用户是否已存在（通过邮箱）
            result = await session.execute(
                select(User).where(User.email == user_data["email"])
            )
            existing = result.scalar_one_or_none()

            if existing:
                print(f"⏭️  用户 {user_data['username']} 已存在，跳过")
                continue

            # 创建新用户
            new_user = User(**user_data)
            session.add(new_user)
            await session.commit()
            print(f"✅ 创建用户: {user_data['username']} ({user_data['email']})")

        # 统计用户数量
        result = await session.execute(select(User))
        users = result.scalars().all()
        count = len(users)
        print(f"\n📊 当前数据库中共有 {count} 个用户")

        # 显示所有用户
        print("\n📋 用户列表:")
        for user in users:
            print(f"   - {user.username} ({user.email}) - Type: {user.user_type}")

        print("\n✨ 初始化完成！")


async def create_new_user(username: str, email: str, password: str, user_type: str = "user"):
    """创建新用户"""
    async with AsyncSessionLocal() as session:
        # 检查邮箱是否已存在
        result = await session.execute(
            select(User).where(User.email == email)
        )
        existing = result.scalar_one_or_none()

        if existing:
            print(f"❌ 邮箱 {email} 已被注册")
            return

        # 创建用户
        hashed_password = pwd_context.hash(password)
        new_user = User(
            id=uuid.uuid4(),
            username=username,
            email=email,
            password=hashed_password,
            user_type=user_type,
            is_active=True,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )

        session.add(new_user)
        await session.commit()
        print(f"✅ 创建用户: {username} ({email})")


async def list_users():
    """列出所有用户"""
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User))
        users = result.scalars().all()

        print(f"\n📋 数据库中共有 {len(users)} 个用户:")
        for user in users:
            print(f"   - {user.username} ({user.email})")
            print(f"     ID: {user.id}")
            print(f"     Type: {user.user_type}, Active: {user.is_active}")
            print(f"     Created: {user.created_at}")


if __name__ == "__main__":
    import sys

    print("=" * 50)
    print("🚀 用户数据初始化脚本 (PostgreSQL)")
    print("=" * 50)

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "create":
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

        elif command == "list":
            # 列出所有用户
            asyncio.run(list_users())

        else:
            print(f"❌ 未知命令: {command}")
            print("可用命令: init, create, list")
            sys.exit(1)
    else:
        # 初始化默认用户
        asyncio.run(init_users())
