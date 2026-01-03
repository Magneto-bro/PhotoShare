from fastapi import Depends, HTTPException, status

from src.services.auth import auth_service
from src.entity.models import RoleEnum

def role_required(*roles: RoleEnum):
    async def role_dependency(user=Depends(auth_service.get_current_user)):
        if user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        return user
    return role_dependency


