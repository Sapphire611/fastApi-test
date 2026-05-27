import asyncio
import logging
import uuid
from datetime import datetime, timezone
from typing import Optional, List
import bcrypt
from supabase import Client

from app.core.config import settings
from app.schemas.user import UserCreate, UserUpdate
from app.models.user import User
from app.core.crypto import hash_password_sha256, is_sha256_hex

logger = logging.getLogger(__name__)


class UserService:
    def __init__(self, supabase: Client):
        self.supabase = supabase

    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        return bcrypt.checkpw(password.encode(), hashed.encode())

    @staticmethod
    def get_password_hash(password: str) -> str:
        pwd = password.encode()
        if len(pwd) > 72:
            pwd = pwd[:72]
        return bcrypt.hashpw(pwd, bcrypt.gensalt()).decode()

    async def _run(self, query):
        return await asyncio.to_thread(query.execute)

    async def get_user_by_id(self, user_id: str) -> Optional[User]:
        result = await self._run(
            self.supabase.table("users").select("*").eq("id", user_id)
        )
        return User(result.data[0]) if result.data else None

    async def get_user_by_email(self, email: str) -> Optional[User]:
        result = await self._run(
            self.supabase.table("users").select("*").eq("email", email)
        )
        return User(result.data[0]) if result.data else None

    async def get_user_by_username(self, username: str) -> Optional[User]:
        result = await self._run(
            self.supabase.table("users").select("*").eq("username", username)
        )
        return User(result.data[0]) if result.data else None

    async def get_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        result = await self._run(
            self.supabase.table("users")
            .select("*")
            .range(skip, skip + limit - 1)
            .order("created_at", desc=True)
        )
        return [User(row) for row in (result.data or [])]

    async def create_user(self, user: UserCreate) -> User:
        user_dict = user.model_dump()
        raw_password = user_dict.pop("password")

        # Double hash: SHA-256 (frontend pattern) → bcrypt (storage)
        sha256_hex = hash_password_sha256(raw_password)
        hashed_password = self.get_password_hash(sha256_hex)

        now = datetime.now(timezone.utc).isoformat()
        row = {
            **user_dict,
            "id": str(uuid.uuid4()),
            "password": hashed_password,
            "is_active": True,
            "created_at": now,
            "updated_at": now,
        }

        result = await self._run(self.supabase.table("users").insert(row))
        return User(result.data[0])

    async def update_user(self, user_id: str, user: UserUpdate) -> Optional[User]:
        db_user = await self.get_user_by_id(user_id)
        if not db_user:
            return None

        update_data = user.model_dump(exclude_unset=True)

        if "password" in update_data:
            sha256_hex = hash_password_sha256(update_data["password"])
            update_data["password"] = self.get_password_hash(sha256_hex)

        update_data["updated_at"] = datetime.now(timezone.utc).isoformat()

        result = await self._run(
            self.supabase.table("users").update(update_data).eq("id", user_id)
        )
        return User(result.data[0]) if result.data else None

    async def delete_user(self, user_id: str) -> bool:
        db_user = await self.get_user_by_id(user_id)
        if not db_user:
            return False

        await self._run(self.supabase.table("users").delete().eq("id", user_id))
        return True

    async def authenticate_user(self, login: str, password: str) -> tuple[Optional[User], str]:
        # Support both email and username login
        if "@" in login:
            user = await self.get_user_by_email(login)
        else:
            user = await self.get_user_by_username(login)
        if not user:
            return None, f"User not found: {login}"

        stored = user.password or ""
        is_sha = is_sha256_hex(password)
        sha256_if_plain = "" if is_sha else hash_password_sha256(password)

        # 1) New format: frontend sends SHA-256 hex, stored = bcrypt(SHA256)
        if self.verify_password(password, stored):
            return user, "ok (new format)"

        # 2) Old frontend (sends plain text): SHA-256 it, then bcrypt compare
        if not is_sha:
            if self.verify_password(sha256_if_plain, stored):
                new_hash = self.get_password_hash(sha256_if_plain)
                await self._run(
                    self.supabase.table("users")
                    .update({"password": new_hash})
                    .eq("id", user.id)
                )
                return user, "ok (auto-upgraded)"

        # Diagnostic info
        return None, (
            f"Password mismatch. "
            f"input_len={len(password)} is_sha256={is_sha} "
            f"stored_pfx={stored[:7]} salt_set={bool(settings.PASSWORD_SALT)} "
            f"stored_is_bcrypt={stored.startswith('$2')}"
            + (f" sha256_of_input={sha256_if_plain[:16]}..." if sha256_if_plain else "")
        )

    async def migrate_password(self, username: str, plain_password: str) -> bool:
        """Upgrade a user from old format bcrypt(plain) to bcrypt(SHA256(plain+salt))"""
        user = await self.get_user_by_username(username)
        if not user:
            return False

        stored = user.password or ""

        # Verify the plain password matches old-format stored bcrypt
        if not self.verify_password(plain_password, stored):
            logger.warning("Migration failed: plain password does not match stored hash for %s", username)
            return False

        sha256_hex = hash_password_sha256(plain_password)
        new_hash = self.get_password_hash(sha256_hex)
        await self._run(
            self.supabase.table("users")
            .update({"password": new_hash})
            .eq("id", user.id)
        )
        logger.info("Password migrated to SHA-256+bcrypt for user: %s", username)
        return True
