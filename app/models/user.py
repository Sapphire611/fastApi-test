from datetime import datetime
from typing import Any, Optional


class User:
    """User model backed by a Supabase row dict"""

    def __init__(self, data: dict[str, Any]):
        self._data = data

    @property
    def id(self) -> str:
        return self._data["id"]

    @property
    def username(self) -> str:
        return self._data["username"]

    @property
    def email(self) -> str:
        return self._data["email"]

    @property
    def password(self) -> str:
        return self._data["password"]

    @property
    def user_type(self) -> str:
        return self._data.get("user_type", "user")

    @property
    def profile_name(self) -> Optional[str]:
        return self._data.get("profile_name")

    @property
    def profile_phone(self) -> Optional[str]:
        return self._data.get("profile_phone")

    @property
    def profile_avatar(self) -> Optional[str]:
        return self._data.get("profile_avatar")

    @property
    def is_active(self) -> bool:
        return self._data.get("is_active", True)

    @property
    def created_at(self) -> Optional[datetime]:
        val = self._data.get("created_at")
        if isinstance(val, str):
            return datetime.fromisoformat(val.replace("Z", "+00:00"))
        return val

    @property
    def updated_at(self) -> Optional[datetime]:
        val = self._data.get("updated_at")
        if isinstance(val, str):
            return datetime.fromisoformat(val.replace("Z", "+00:00"))
        return val

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "user_type": self.user_type,
            "profile_name": self.profile_name,
            "profile_phone": self.profile_phone,
            "profile_avatar": self.profile_avatar,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
