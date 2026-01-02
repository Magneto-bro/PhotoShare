from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.entity.models import Photo


async def get_photo_by_id(photo_id: int, db: AsyncSession):
    result = await db.execute(
        select(Photo).where(Photo.id == photo_id)
    )
    return result.scalar_one_or_none()


async def delete_photo(photo: Photo, db: AsyncSession):
    await db.delete(photo)
    await db.commit()


async def update_photo(
    photo: Photo,
    description: str | None,
    db: AsyncSession,
):
    if description is not None:
        photo.description = description

    await db.commit()
    await db.refresh(photo)
    return photo
