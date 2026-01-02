from fastapi import HTTPException
from sqlalchemy import select
from src.entity.models import RoleEnum, Tag
from src.repository.photos import create_photo, get_photo
from src.repository.tags import create_tag, get_tag_by_name
from src.schemas.photo import PhotoCreate

async def get_owned_photo(db, photo_id: int, user):
    photo = await get_photo(db, photo_id)

    if not photo:
        raise HTTPException(404, "Photo not found")

    if photo.user_id != user.id and user.role not in [RoleEnum.admin, RoleEnum.moderator]:
        raise HTTPException(403, "Not enough permissions")

    return photo

async def assign_tags_to_photo(db, photo, tag_names: list[str]):
    if len(tag_names) > 5:
        raise HTTPException(status_code=400, detail="Max 5 tags allowed")

    tags = []
    seen = set()
    for name in tag_names:
        name = name.strip().lower()
        if name in seen:
            continue
        seen.add(name)

        tag_obj = await get_tag_by_name(db, name)
        if not tag_obj:
            tag_obj = await create_tag(db, name)
        tags.append(tag_obj)

    photo.tags = tags
    await db.commit()
    await db.refresh(photo)
    return photo


async def upload_photo_service(db, data: PhotoCreate, user):
    photo = await create_photo(db, data, user.id)

    if data.tags:
        photo = await assign_tags_to_photo(db, photo, data.tags)

    return photo

