from typing import Optional, List
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorDatabase
from passlib.context import CryptContext
from bson import ObjectId
from app.schemas.user import UserCreate, UserUpdate
from app.models.user import UserModel

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    def __init__(self, database: AsyncIOMotorDatabase):
        self.db = database
        self.collection = database.users

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

    async def get_user_by_id(self, user_id: str) -> Optional[UserModel]:
        """Get a user by ID"""
        user_doc = await self.collection.find_one({"_id": ObjectId(user_id)})
        if user_doc:
            user_doc["_id"] = str(user_doc["_id"])
            return UserModel(**user_doc)
        return None

    async def get_user_by_email(self, email: str) -> Optional[UserModel]:
        """Get a user by email"""
        user_doc = await self.collection.find_one({"email": email})
        if user_doc:
            user_doc["_id"] = str(user_doc["_id"])
            return UserModel(**user_doc)
        return None

    async def get_user_by_username(self, username: str) -> Optional[UserModel]:
        """Get a user by username"""
        user_doc = await self.collection.find_one({"username": username})
        if user_doc:
            user_doc["_id"] = str(user_doc["_id"])
            return UserModel(**user_doc)
        return None

    async def get_users(self, skip: int = 0, limit: int = 100) -> List[UserModel]:
        """Get a list of users"""
        cursor = self.collection.find().skip(skip).limit(limit)
        users = []
        async for user_doc in cursor:
            user_doc["_id"] = str(user_doc["_id"])
            users.append(UserModel(**user_doc))
        return users

    async def create_user(self, user: UserCreate) -> UserModel:
        """Create a new user"""
        user_dict = user.model_dump()
        user_dict["password"] = self.get_password_hash(user_dict.pop("password"))
        user_dict["createdAt"] = datetime.utcnow()
        user_dict["updatedAt"] = datetime.utcnow()

        result = await self.collection.insert_one(user_dict)
        user_dict["_id"] = str(result.inserted_id)

        return UserModel(**user_dict)

    async def update_user(self, user_id: str, user: UserUpdate) -> Optional[UserModel]:
        """Update a user"""
        update_data = {k: v for k, v in user.model_dump().items() if v is not None}

        if "password" in update_data:
            update_data["password"] = self.get_password_hash(update_data["password"])

        update_data["updatedAt"] = datetime.utcnow()

        await self.collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": update_data}
        )

        return await self.get_user_by_id(user_id)

    async def delete_user(self, user_id: str) -> bool:
        """Delete a user"""
        result = await self.collection.delete_one({"_id": ObjectId(user_id)})
        return result.deleted_count > 0

    async def authenticate_user(self, username: str, password: str) -> Optional[UserModel]:
        """Authenticate a user"""
        user = await self.get_user_by_username(username)
        if not user:
            return None
        if not self.verify_password(password, user.password):
            return None
        return user

# Dependency to get user service
def get_user_service(database: AsyncIOMotorDatabase) -> UserService:
    """Get user service instance"""
    return UserService(database)
