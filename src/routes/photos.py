from fastapi import APIRouter, Depends, HTTPException

from src.schemas.photo import PhotoCreate, PhotoResponse, PhotoUpdate
from src.database.db import get_db
from src.services.auth import get_current_user
from src.services.photos import get_owned_photo
from src.repository.photos import create_photo, get_photo, update_photo, delete_photo

router = APIRouter(prefix="/photos", tags=["photos"])


@router.post("/", response_model=PhotoResponse)
async def upload_photo(
    data: PhotoCreate,
    user=Depends(get_current_user),
    db=Depends(get_db)
):
    return await create_photo(db, data, user.id)


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
    user=Depends(get_current_user),
    db=Depends(get_db)
):
    photo = await get_owned_photo(db, photo_id, user)
    return await update_photo(db, photo, data.description)


@router.delete("/{photo_id}")
async def delete_photo_endpoint(
    photo_id: int,
    user=Depends(get_current_user),
    db=Depends(get_db)
):
    photo = await get_owned_photo(db, photo_id, user)
    await delete_photo(db, photo)
    return {"detail": "Photo deleted"}
