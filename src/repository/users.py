from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.entity.models import User, RoleEnum
from passlib.context import CryptContext

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
