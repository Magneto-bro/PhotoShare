from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from src.schemas.photo import PhotoCreate, PhotoResponse, PhotoUpdate
from src.database.db import get_db
from src.services.auth import auth_service
from src.services.photos import assign_tags_to_photo, get_owned_photo, upload_photo_service
from src.repository.photos import create_photo, get_photo, update_photo, delete_photo
from sqlalchemy.ext.asyncio import AsyncSession
from src.repository import photos as repository_photos
from src.services.auth import auth_service
from src.services.cloudinary_service import get_transformed_url, upload_image
from src.entity.models import Photo


router = APIRouter(prefix="/photos", tags=["photos"])


@router.get("/{photo_id}", response_model=PhotoResponse)
async def get_photo_by_id(photo_id: int, db=Depends(get_db)):
    photo = await get_photo(db, photo_id)
    if not photo:
        raise HTTPException(404)
    return photo


@router.put("/{photo_id}", response_model=PhotoResponse)
async def edit_photo(
    photo_id: int,
    data: PhotoUpdate,
    user=Depends(auth_service.get_current_user),
    db=Depends(get_db)
):
    photo = await get_owned_photo(db, photo_id, user)
    return await update_photo(db, photo, data.description)


@router.delete("/{photo_id}")
async def delete_photo_endpoint(
    photo_id: int,
    user=Depends(auth_service.get_current_user),
    db=Depends(get_db)
):
    photo = await get_owned_photo(db, photo_id, user)
    await delete_photo(db, photo)
    return {"detail": "Photo deleted"}


@router.post("/", status_code=201)
async def upload_photo(
    file: UploadFile = File(...),
    description: str = "",
    db: AsyncSession = Depends(get_db),
    user=Depends(auth_service.get_current_user)
):
    url = upload_image(file.file)
    photo = Photo(
        image_url=url,
        description=description,
        owner_id=user.id
    )
    db.add(photo)
    await db.commit()
    await db.refresh(photo)
    return photo


@router.post("/{photo_id}/transform", response_model=PhotoResponse)
async def transform_photo(
    photo_id: int,
    width: int = 500,
    height: int = 500,
    db: AsyncSession = Depends(get_db),
    user=Depends(auth_service.get_current_user)
):
    photo = await repository_photos.get_photo_by_id(photo_id, db)
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")
    if photo.owner_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    import os
    public_id = os.path.splitext(os.path.basename(photo.image_url))[0]
    transformed_url = get_transformed_url(photo.image_url, width, height)

    return PhotoResponse(
        id=photo.id,
        image_url=transformed_url,
        description=photo.description,
        created_at=photo.created_at
    )
