from typing import Optional, List
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from passlib.context import CryptContext
import uuid

from app.schemas.user import UserCreate, UserUpdate
from app.models.user import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a password against a hash"""
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        """Hash a password"""
        # bcrypt has a 72 byte limit, truncate if necessary
        password_bytes = password.encode('utf-8')
        if len(password_bytes) > 72:
            password = password_bytes[:72].decode('utf-8', errors='ignore')
        return pwd_context.hash(password)

    async def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Get a user by ID"""
        try:
            user_uuid = uuid.UUID(user_id)
        except ValueError:
            return None

        result = await self.db.execute(select(User).where(User.id == user_uuid))
        return result.scalar_one_or_none()

    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Get a user by email"""
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def get_user_by_username(self, username: str) -> Optional[User]:
        """Get a user by username"""
        result = await self.db.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()

    async def get_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Get a list of users"""
        result = await self.db.execute(select(User).offset(skip).limit(limit))
        return list(result.scalars().all())

    async def create_user(self, user: UserCreate) -> User:
        """Create a new user"""
        user_dict = user.model_dump()
        hashed_password = self.get_password_hash(user_dict.pop("password"))

        db_user = User(
            username=user_dict["username"],
            email=user_dict["email"],
            password=hashed_password,
            user_type=user_dict.get("user_type", "user"),
            is_active=user_dict.get("is_active", True),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        self.db.add(db_user)
        await self.db.flush()

        return db_user

    async def update_user(self, user_id: str, user: UserUpdate) -> Optional[User]:
        """Update a user"""
        try:
            user_uuid = uuid.UUID(user_id)
        except ValueError:
            return None

        db_user = await self.get_user_by_id(user_id)
        if not db_user:
            return None

        update_data = user.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            if field == "password":
                setattr(db_user, field, self.get_password_hash(value))
            else:
                setattr(db_user, field, value)

        db_user.updated_at = datetime.utcnow()
        await self.db.flush()

        return db_user

    async def delete_user(self, user_id: str) -> bool:
        """Delete a user"""
        try:
            user_uuid = uuid.UUID(user_id)
        except ValueError:
            return False

        db_user = await self.get_user_by_id(user_id)
        if not db_user:
            return False

        await self.db.delete(db_user)
        await self.db.flush()

        return True

    async def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """Authenticate a user"""
        user = await self.get_user_by_username(username)
        if not user:
            return None
        if not self.verify_password(password, user.password):
            return None
        return user

# Dependency to get user service
def get_user_service(db: AsyncSession) -> UserService:
    """Get user service instance"""
    return UserService(db)
