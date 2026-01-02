from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.entity.models import Tag


async def get_tag_by_name(db: AsyncSession, name: str) -> Tag | None:
    result = await db.execute(select(Tag).where(Tag.name == name))
    return result.scalar_one_or_none()


async def create_tag(db: AsyncSession, name: str) -> Tag:
    tag_obj = Tag(name=name)
    db.add(tag_obj)
    await db.commit()      
    await db.refresh(tag_obj)
    return tag_obj


async def get_all_tags(db: AsyncSession) -> list[Tag]:
    result = await db.execute(select(Tag))
    return result.scalars().all()
