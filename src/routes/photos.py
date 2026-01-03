from fastapi import APIRouter, Depends, HTTPException

from src.schemas.photo import PhotoCreate, PhotoResponse, PhotoUpdate
from src.database.db import get_db
from src.services.auth import auth_service
from src.services.photos import assign_tags_to_photo, get_owned_photo, upload_photo_service
from src.repository.photos import create_photo, get_photo, update_photo, delete_photo

router = APIRouter(prefix="/photos", tags=["photos"])


@router.post("/", response_model=PhotoResponse)
async def upload_photo(
    data: PhotoCreate,
    user=Depends(auth_service.get_current_user
),
    db=Depends(get_db)
):
    photo = await upload_photo_service(db, data, user)
    return photo



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
