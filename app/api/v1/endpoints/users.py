from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.core.database import get_database
from app.crud.user import UserCRUD, get_user_crud
from app.schemas.user import UserCreate, UserUpdate, UserResponse, UserLogin, Token

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate, db=Depends(get_database)):
    """Register a new user"""
    user_crud = get_user_crud(db)

    # Check if user already exists
    existing_user = await user_crud.get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    existing_username = await user_crud.get_user_by_username(user.username)
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )

    # Create new user
    new_user = await user_crud.create_user(user)
    return UserResponse(**new_user.model_dump())

@router.post("/login", response_model=Token)
async def login(user_login: UserLogin, db=Depends(get_database)):
    """Login user"""
    user_crud = get_user_crud(db)
    user = await user_crud.authenticate_user(user_login.username, user_login.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.isActive:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )

    # For now, return username as token (TODO: implement JWT)
    return Token(access_token=user.username, token_type="bearer")

@router.get("/", response_model=List[UserResponse])
async def get_users(skip: int = 0, limit: int = 100, db=Depends(get_database)):
    """Get all users"""
    user_crud = get_user_crud(db)
    users = await user_crud.get_users(skip=skip, limit=limit)
    return [UserResponse(**user.model_dump()) for user in users]

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: str, db=Depends(get_database)):
    """Get a user by ID"""
    user_crud = get_user_crud(db)
    user = await user_crud.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return UserResponse(**user.model_dump())

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: str, user: UserUpdate, db=Depends(get_database)):
    """Update a user"""
    user_crud = get_user_crud(db)

    # Check if user exists
    existing_user = await user_crud.get_user_by_id(user_id)
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Check if email is already taken by another user
    if user.email:
        email_user = await user_crud.get_user_by_email(user.email)
        if email_user and email_user.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

    updated_user = await user_crud.update_user(user_id, user)
    return UserResponse(**updated_user.model_dump())

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: str, db=Depends(get_database)):
    """Delete a user"""
    user_crud = get_user_crud(db)
    success = await user_crud.delete_user(user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return None
