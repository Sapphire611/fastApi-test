from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    email: EmailStr
    password: str = Field(min_length=6)
    user_type: str = Field(default="user", pattern=r"^(admin|user)$")
    profile_name: Optional[str] = None
    profile_phone: Optional[str] = None
    profile_avatar: Optional[str] = None


class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=20)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=6)
    user_type: Optional[str] = Field(None, pattern=r"^(admin|user)$")
    profile_name: Optional[str] = None
    profile_phone: Optional[str] = None
    profile_avatar: Optional[str] = None
    is_active: Optional[bool] = None


class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    user_type: str
    profile_name: Optional[str] = None
    profile_phone: Optional[str] = None
    profile_avatar: Optional[str] = None
    is_active: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class UserLogin(BaseModel):
    username: str
    password: str


class MigratePassword(BaseModel):
    username: str
    plain_password: str = Field(min_length=1)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
