from pydantic import BaseModel, EmailStr, Field, ConfigDict, field_serializer
from typing import Optional
from datetime import datetime
from uuid import UUID

class UserBase(BaseModel):
    """Base user schema"""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    user_type: str = "user"
    is_active: bool = True

class UserCreate(UserBase):
    """Schema for creating a user"""
    password: str = Field(..., min_length=6)

class UserUpdate(BaseModel):
    """Schema for updating a user"""
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    user_type: Optional[str] = None
    is_active: Optional[bool] = None
    password: Optional[str] = Field(None, min_length=6)

class UserInDB(UserBase):
    """Schema for user in database (includes password)"""
    id: UUID
    password: str
    created_at: datetime
    updated_at: datetime

    @field_serializer('id')
    def serialize_id(self, id: UUID) -> str:
        return str(id)

    model_config = ConfigDict(from_attributes=True)

class UserResponse(BaseModel):
    """Schema for user response (excludes password)"""
    id: UUID
    username: str
    email: EmailStr
    user_type: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    @field_serializer('id')
    def serialize_id(self, id: UUID) -> str:
        return str(id)

    model_config = ConfigDict(from_attributes=True)

class UserLogin(BaseModel):
    """Schema for user login"""
    username: str
    password: str

class Token(BaseModel):
    """Schema for token response"""
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    """Schema for token data"""
    username: Optional[str] = None
