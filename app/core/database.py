import logging
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.exc import OperationalError
from typing import AsyncGenerator
from app.core.config import settings

logger = logging.getLogger(__name__)

# Create async engine
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,  # Set to False in production
    future=True
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

# Base class for models
Base = declarative_base()

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency to get database session"""
    try:
        async with AsyncSessionLocal() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()
    except OperationalError as e:
        _diagnose_db_error(e)
        raise
    except OSError as e:
        logger.error(
            "PostgreSQL server not reachable at %s:%s. "
            "Check that the server is running and POSTGRES_SERVER/POSTGRES_PORT are correct.",
            settings.POSTGRES_SERVER,
            settings.POSTGRES_PORT,
        )
        raise

def _diagnose_db_error(e: OperationalError) -> None:
    """Log the specific PostgreSQL connection failure reason"""
    orig = getattr(e, "orig", None)
    if orig is None:
        logger.error(
            "PostgreSQL connection failed: %s. "
            "Check that POSTGRES_SERVER, POSTGRES_PORT, POSTGRES_USER, "
            "POSTGRES_PASSWORD, and POSTGRES_DB are set correctly.",
            e,
        )
        return

    pgcode = getattr(orig, "pgcode", None)

    if pgcode == "28P01":
        logger.error(
            "PostgreSQL authentication failed: invalid username or password. "
            "Check POSTGRES_USER=%r and POSTGRES_PASSWORD.",
            settings.POSTGRES_USER,
        )
    elif pgcode == "3D000":
        logger.error(
            "PostgreSQL database not found: %r. "
            "Check POSTGRES_DB setting.",
            settings.POSTGRES_DB,
        )
    elif isinstance(orig, OSError):
        logger.error(
            "PostgreSQL server not reachable at %s:%s. "
            "Check that the server is running and POSTGRES_SERVER/POSTGRES_PORT are correct.",
            settings.POSTGRES_SERVER,
            settings.POSTGRES_PORT,
        )
    else:
        logger.error(
            "PostgreSQL connection failed (pgcode=%s): %s. "
            "Check POSTGRES_SERVER, POSTGRES_PORT, POSTGRES_USER, "
            "POSTGRES_PASSWORD, and POSTGRES_DB settings.",
            pgcode,
            orig,
        )


async def init_db() -> None:
    """Initialize database tables"""
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database connected and tables initialized successfully")
    except OperationalError as e:
        _diagnose_db_error(e)
        raise
    except OSError as e:
        logger.error(
            "PostgreSQL server not reachable at %s:%s. "
            "Check that the server is running and POSTGRES_SERVER/POSTGRES_PORT are correct.",
            settings.POSTGRES_SERVER,
            settings.POSTGRES_PORT,
        )
        raise

async def close_db() -> None:
    """Close database connection"""
    await engine.dispose()
