from fastapi import APIRouter, Depends, HTTPException, status
from supabase import Client
from typing import List
from app.core.database import get_supabase
from app.services.user_service import UserService
from app.core.config import settings
from app.schemas.user import UserCreate, UserUpdate, UserResponse, UserLogin, LoginResponse

router = APIRouter()


def get_user_service(supabase: Client = Depends(get_supabase)) -> UserService:
    return UserService(supabase)


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate, svc: UserService = Depends(get_user_service)):
    if await svc.get_user_by_email(user.email):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    if await svc.get_user_by_username(user.username):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Username already taken")

    new_user = await svc.create_user(user)
    return UserResponse.model_validate(new_user.to_dict())


@router.post("/login", response_model=LoginResponse)
async def login(user_login: UserLogin, svc: UserService = Depends(get_user_service)):
    user, diag = await svc.authenticate_user(user_login.username, user_login.password)
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail=diag)
    if not user.is_active:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Inactive user")

    return LoginResponse(
        access_token=user.username,
        token_type="bearer",
        user=UserResponse.model_validate(user.to_dict()),
    )


@router.get("/", response_model=List[UserResponse])
async def list_users(
    skip: int = 0,
    limit: int = 100,
    svc: UserService = Depends(get_user_service),
):
    users = await svc.get_users(skip=skip, limit=limit)
    return [UserResponse.model_validate(u.to_dict()) for u in users]


@router.post("/debug-password")
async def debug_password(user_login: UserLogin):
    """Show the two-layer encryption steps for a given password (no DB access)"""
    from app.core.crypto import hash_password_sha256
    from app.services.user_service import UserService
    sha256 = hash_password_sha256(user_login.password)
    bcrypt_hash = UserService.get_password_hash(sha256)
    return {
        "input": user_login.password,
        "salt": settings.PASSWORD_SALT,
        "sha256_hex": sha256,
        "bcrypt_of_sha256": bcrypt_hash,
    }


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: str, svc: UserService = Depends(get_user_service)):
    user = await svc.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")
    return UserResponse.model_validate(user.to_dict())


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: str,
    payload: UserUpdate,
    svc: UserService = Depends(get_user_service),
):
    if not await svc.get_user_by_id(user_id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")

    if payload.email:
        conflict = await svc.get_user_by_email(payload.email)
        if conflict and conflict.id != user_id:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    updated = await svc.update_user(user_id, payload)
    return UserResponse.model_validate(updated.to_dict())


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: str, svc: UserService = Depends(get_user_service)):
    if not await svc.delete_user(user_id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")
    return None
