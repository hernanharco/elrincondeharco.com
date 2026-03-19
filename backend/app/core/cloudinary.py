import cloudinary
import cloudinary.uploader
from fastapi import UploadFile
from app.core.config import settings

cloudinary.config(
    cloud_name=settings.cloudinary_cloud_name,
    api_key=settings.cloudinary_api_key,
    api_secret=settings.cloudinary_api_secret,
    secure=True
)

async def upload_image(file: UploadFile) -> str:
    """
    Sube una imagen a Cloudinary y retorna la URL pública segura (https).
    Nunca retorna binario ni ruta local.
    """
    contents = await file.read()
    result = cloudinary.uploader.upload(
        contents,
        folder="elrincondelharco",
        resource_type="image"
    )
    return result["secure_url"]  # siempre str
