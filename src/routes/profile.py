
from fastapi import APIRouter, Depends , HTTPException

from src.services.auth import auth_service
from src.entity.models import User
from src.schemas.user import PublicProfile, PrivateProfile ,UserUpdate
from src.database.db import get_db
from src.repository import users as repository_users

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
router = APIRouter(prefix="/profile", tags=["profile"])

@router.get("/{username}", response_model=PublicProfile)
async def public_profile(
    username: str,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(User).where(User.username == username, User.is_banned == False)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="user not found")

    return {
        "username": user.username,
        "full_name": user.full_name,
        "created_at": user.created_at,
        "photos_count": len(user.photos),
    }

@router.get("/profile/me", response_model=PrivateProfile)
async def my_profile(
    current_user: User = Depends(auth_service.get_current_user),
):
    return current_user

@router.put("/me", response_model=PrivateProfile)
async def update_my_profile(
    data: UserUpdate,
    current_user: User = Depends(auth_service.get_current_user),
    db: AsyncSession = Depends(get_db),
):
    updated_user = await repository_users.update_user(
        current_user, data, db
    )
    return updated_user
