from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    """Base user schema"""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    userType: str = "user"
    isActive: bool = True

class UserCreate(UserBase):
    """Schema for creating a user"""
    password: str = Field(..., min_length=6)

class UserUpdate(BaseModel):
    """Schema for updating a user"""
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    userType: Optional[str] = None
    isActive: Optional[bool] = None
    password: Optional[str] = Field(None, min_length=6)

class UserInDB(UserBase):
    """Schema for user in database (includes password)"""
    id: str = Field(..., alias="_id")
    password: str
    createdAt: datetime
    updatedAt: datetime

    class Config:
        populate_by_name = True

class UserResponse(BaseModel):
    """Schema for user response (excludes password)"""
    id: str = Field(..., alias="_id")
    username: str
    email: EmailStr
    userType: str
    isActive: bool
    createdAt: datetime
    updatedAt: datetime

    class Config:
        populate_by_name = True

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
