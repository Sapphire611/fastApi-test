from pydantic import BaseModel, Field, EmailStr, ConfigDict, field_serializer
from typing import Optional
from datetime import datetime

class UserModel(BaseModel):
    """MongoDB User Model"""
    id: str = Field(..., alias="_id")
    username: str
    email: EmailStr
    password: str
    userType: str = "user"  # admin, user
    isActive: bool = True
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(populate_by_name=True)

    @field_serializer('createdAt', 'updatedAt')
    def serialize_datetime(self, dt: datetime, _info):
        return dt.isoformat()
