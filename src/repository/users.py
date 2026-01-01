from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.entity.models import User, RoleEnum
from passlib.context import CryptContext
from src.schemas.user import UserUpdate
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


async def create_user(email: str, username: str, password: str, db: AsyncSession):
    hashed_password = pwd_context.hash(password)
    result = await db.execute(select(User))
    first_user_exists = result.scalar_one_or_none() is not None
    role = RoleEnum.admin if not first_user_exists else RoleEnum.user
    user = User(
        email=email, username=username, hashed_password=hashed_password, role=role
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def get_user_by_email(email: str, db: AsyncSession):
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def get_user_by_id(user_id: int, db: AsyncSession):
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def get_first_user(db: AsyncSession):
    result = await db.execute(select(User).order_by(User.id))
    return result.scalar_one_or_none()

async def update_user(
    user: User,
    data: UserUpdate,
    db: AsyncSession,):
    if data.username is not None:
        user.username = data.username

    if data.full_name is not None:
        user.full_name = data.full_name

    if data.email is not None:
        user.email = data.email

    await db.commit()
    await db.refresh(user)
    return user

async def ban_user(user:User,db:AsyncSession):
    user.is_banned=True
    user.is_active =False
    await db.commit()
    await db.refresh(user)
    return user

async def unban_user(user:User,db:AsyncSession):
    user.is_banned=False
    user.is_active =True
    await db.commit()
    await db.refresh(user)
    return user
