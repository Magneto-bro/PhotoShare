import os
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.schemas.photo import PhotoResponse, PhotoUpdate
from src.entity.models import Photo
from src.services.auth import auth_service
from src.services.cloudinary_service import get_transformed_url, upload_image
from src.repository import photos as repository_photos
from src.services.photos import get_owned_photo

router = APIRouter(prefix="/photos", tags=["photos"])



@router.get("/{photo_id}")
async def get_photo(photo_id: int, db: AsyncSession = Depends(get_db)):
    photo = await repository_photos.get_photo_by_id(photo_id, db)
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")
    return photo


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PhotoResponse)
async def upload_photo(
    file: UploadFile = File(...),
    description: str = "",
    db: AsyncSession = Depends(get_db),
    user = Depends(auth_service.get_current_user)
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


@router.get("/{photo_id}", response_model=PhotoResponse)
async def get_photo_by_id(photo_id: int, db=Depends(get_db)):
    photo = await get_photo(photo_id, db)
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
    return await repository_photos.update_photo(db, photo, data.description)


@router.delete("/{photo_id}")
async def delete_photo_endpoint(
    photo_id: int,
    user=Depends(auth_service.get_current_user),
    db=Depends(get_db)
):
    photo = await get_owned_photo(db, photo_id, user)
    await repository_photos.delete_photo(db, photo)
    return {"detail": "Photo deleted"}


@router.post("/{photo_id}/transform", response_model=PhotoResponse)
async def transform_photo(
    photo_id: int,
    width: int = 500,
    height: int = 500,
    db: AsyncSession = Depends(get_db),
    user = Depends(auth_service.get_current_user)
):
    photo = await repository_photos.get_photo(db, photo_id)
    if not photo or photo.owner_id != user.id:
        raise HTTPException(status_code=404, detail="Photo not found or not authorized")

    # Витягуємо public_id для Cloudinary
    public_id = os.path.splitext(os.path.basename(photo.image_url))[0]
    transformed_url = get_transformed_url(public_id, width, height)
     
    return PhotoResponse(
        id=photo.id,
        image_url=transformed_url,
        description=photo.description,
        created_at=photo.created_at
    )
