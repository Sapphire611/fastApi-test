import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.main import app
from app.core import database

# Use SQLite in-memory database for testing to avoid connection pool issues
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

test_engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=False,
    future=True
)

TestSessionLocal = async_sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)


@pytest.fixture(scope="session")
async def setup_test_database():
    """Setup test database tables"""
    async with test_engine.begin() as conn:
        await conn.run_sync(database.Base.metadata.create_all)
    yield
    # Clean up at session end
    async with test_engine.begin() as conn:
        await conn.run_sync(database.Base.metadata.drop_all)
    await test_engine.dispose()


@pytest.fixture(scope="function")
async def client(setup_test_database):
    """Create an async test client with proper cleanup"""
    # Override the database dependency
    async def override_get_db():
        async with TestSessionLocal() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise

    app.dependency_overrides[database.get_db] = override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()


