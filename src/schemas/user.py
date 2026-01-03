from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from src.entity.models import RoleEnum

class UserSchema(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=6, max_length=8)
    role: RoleEnum = RoleEnum.user


class UserResponse(BaseModel):
    id: int = 1
    username: str
    email: EmailStr

    class Config:
        from_attributes = True


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    
    
class RequestEmail(BaseModel):
    email: EmailStr    


class PublicProfile(BaseModel):
    username: str
    full_name: str | None
    created_at: datetime
    photos_count: int

class PrivateProfile(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None
    created_at: datetime

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    username: str | None = Field(default=None, min_length=3, max_length=50)
    full_name: str | None = Field(default=None, max_length=100)
    email: EmailStr | None = None

class AdminUserView(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str
    is_active: bool
    is_banned: bool
    created_at: datetime

    class Config:
        from_attributes = True
