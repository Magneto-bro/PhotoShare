from fastapi import HTTPException
from src.entity.models import RoleEnum
from src.repository.photos import get_photo


async def get_owned_photo(db, photo_id: int, user):
    photo = await get_photo(db, photo_id)

    if not photo:
        raise HTTPException(404, "Photo not found")

    if photo.owner_id != user.id:
        raise HTTPException(403, "Not your photo")

    return photo
