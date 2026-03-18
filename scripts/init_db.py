#!/usr/bin/env python3
"""
Database initialization script for FastAPI PostgreSQL migration.

This script creates all necessary database tables using SQLAlchemy.
Run this script after setting up your PostgreSQL database.
"""

import asyncio
from app.core.database import init_db, close_db
from app.core.config import settings


async def main():
    """Initialize database tables"""
    print(f"Connecting to PostgreSQL database: {settings.POSTGRES_DB}")
    print(f"Database URL: postgresql+asyncpg://{settings.POSTGRES_USER}:***@{settings.POSTGRES_SERVER}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}")

    try:
        await init_db()
        print("✅ Database tables created successfully!")
        print("\n📋 Created tables:")
        from app.models.user import User
        print(f"  - {User.__tablename__} (users)")

        print("\n🎉 Database initialization complete!")
        print("You can now start the FastAPI application.")

    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        print("\n💡 Troubleshooting tips:")
        print("  1. Make sure PostgreSQL is running")
        print("  2. Verify database credentials in .env file")
        print("  3. Ensure the database exists:")
        print(f"     createdb -U {settings.POSTGRES_USER} {settings.POSTGRES_DB}")
        raise

    finally:
        await close_db()
        print("\n🔌 Database connection closed.")


if __name__ == "__main__":
    print("=" * 60)
    print("FastAPI PostgreSQL Database Initialization")
    print("=" * 60)
    asyncio.run(main())
