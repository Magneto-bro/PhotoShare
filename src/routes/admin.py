from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.entity.models import User, RoleEnum
from src.database.db import get_db
from src.repository import users as repository_users
from src.services.dependencies import role_required
from src.schemas.user import AdminUserView
from src.repository import photos as repository_photos
router = APIRouter(prefix="/admin", tags=["admin"])

@router.patch("/users/{user_id}/ban")
async def ban_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(role_required(RoleEnum.admin)),
):
    user = await repository_users.get_user_by_id(user_id, db)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.role == RoleEnum.admin:
        raise HTTPException(status_code=403, detail="Cannot ban admin")

    await repository_users.ban_user(user, db)
    return {"detail": "User banned"}

@router.patch("/users/{user_id}/unban")
async def unban_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(role_required(RoleEnum.admin)),
):
    user = await repository_users.get_user_by_id(user_id, db)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await repository_users.unban_user(user, db)
    return {"detail": "User unbanned"}

@router.get("/users/{user_id}", response_model=AdminUserView)
async def admin_get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(role_required(RoleEnum.admin)),
):
    user = await repository_users.get_user_by_id(user_id, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/photos/{photo_id}/del")
async def admin_delete_photo(
    photo_id: int,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(role_required(RoleEnum.admin)),
):
    photo = await repository_photos.get_photo_by_id(photo_id, db)

    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")

    await repository_photos.delete_photo(photo, db)
    return {"detail": "Photo deleted by admin"}

@router.patch("/photos/{photo_id}")
async def admin_update_photo(
    photo_id: int,
    description: str | None = None,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(role_required(RoleEnum.admin)),
):
    photo = await repository_photos.get_photo_by_id(photo_id, db)

    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")

    updated_photo = await repository_photos.update_photo(
        photo, description, db
    )

    return updated_photo
