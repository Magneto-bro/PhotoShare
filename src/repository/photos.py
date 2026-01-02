from src.entity.models import Photo
from src.schemas.photo import PhotoCreate


async def create_photo(db, data: PhotoCreate, user_id: int):
    photo = Photo(**data.model_dump(), user_id=user_id)
    db.add(photo)
    await db.commit()
    await db.refresh(photo)
    return photo


async def get_photo(db, photo_id: int):
    return await db.get(Photo, photo_id)


async def update_photo(db, photo: Photo, description: str):
    photo.description = description
    await db.commit()
    return photo


async def delete_photo(db, photo: Photo):
    await db.delete(photo)
    await db.commit()
