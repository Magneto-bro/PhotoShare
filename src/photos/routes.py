from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.db import get_db
from src.services.cloudinary_service import upload_image
from src.photos.models import Photo
from src.users.dependencies import get_current_user

router = APIRouter(prefix="/photos", tags=["Photos"])

@router.post("/", status_code=201)
async def upload_photo(
    file: UploadFile = File(...),
    description: str = "",
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user())
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
