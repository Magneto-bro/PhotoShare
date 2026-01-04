import cloudinary
import cloudinary.uploader
from src.conf.config import config as settings

cloudinary.config(
    cloud_name=settings.CLOUDINARY_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET,
    secure=True
)

def upload_image(file):
    result = cloudinary.uploader.upload(file)
    return result["secure_url"]

def get_transformed_url(public_id, width=500, height=500, crop="fill"):
    """
    Генерує URL для вже завантаженого фото з накладеними трансформаціями.
    """
    return cloudinary.CloudinaryImage(public_id).build_url(
        width=width,
        height=height,
        crop=crop,
        gravity="face" # Автоматично фокусується на обличчі
    )
