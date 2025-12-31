from fastapi import APIRouter, Depends
from src.services.auth import auth_service
from src.entity.models import RoleEnum
from src.services.dependencies import role_required


router = APIRouter(prefix="/users", tags=["users"])

@router.get("/admin-only")
async def admin_panel(user=Depends(role_required(RoleEnum.admin))):
    return {"msg": f"Hello, admin {user.username}!"}

@router.get("/me")
async def read_my_profile(user=Depends(auth_service.get_current_user)):
    return {"email": user.email, "username": user.username, "role": user.role}
