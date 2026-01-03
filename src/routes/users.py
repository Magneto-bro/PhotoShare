from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends , HTTPException

from src.services.auth import auth_service
from src.entity.models import RoleEnum , User
from src.services.dependencies import role_required
from src.schemas.user import PublicProfile, PrivateProfile ,UserUpdate
from src.database.db import get_db
from src.repository import users as repository_users

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
router = APIRouter(prefix="/users", tags=["users"])

@router.get("/admin")
async def admin_panel(user=Depends(role_required(RoleEnum.admin))):
    return {"msg": f"Hello, admin {user.username}!"}

