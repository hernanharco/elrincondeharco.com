import os
import re
import asyncio
import cloudinary
import cloudinary.uploader
from fastapi import UploadFile, HTTPException
from app.core.config import settings
import logging

cloudinary.config(
    cloud_name=settings.cloudinary_cloud_name,
    api_key=settings.cloudinary_api_key,
    api_secret=settings.cloudinary_api_secret,
    secure=True
)

logger = logging.getLogger(__name__)

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
IMAGE_MAX_SIZE = 5 * 1024 * 1024   # 5MB para imágenes

async def upload_image(file: UploadFile) -> str:
    try:
        contents = await file.read()
        if not contents:
            raise HTTPException(status_code=400, detail="El archivo está vacío")

        size_limit = IMAGE_MAX_SIZE if (
            file.content_type and file.content_type.startswith('image/')
        ) else MAX_FILE_SIZE
        if len(contents) > size_limit:
            raise HTTPException(
                status_code=413,
                detail=f"Archivo demasiado grande. Máximo {size_limit // (1024*1024)}MB"
            )

        filename = file.filename if file.filename else "archivo"
        
        # 1. Detectar si es PDF
        is_pdf = (
            filename.lower().endswith('.pdf') or 
            (file.content_type == 'application/pdf')
        )

        # 2. Limpiar el nombre del archivo (Quitar espacios y caracteres raros para la URL)
        # Esto convierte "Mi CV 2026.pdf" en "Mi_CV_2026"
        base_name = os.path.splitext(filename)[0]
        clean_name = re.sub(r'[^a-zA-Z0-9_-]', '_', base_name)

        upload_kwargs = {
            "folder": "elrincondelharco",
            "resource_type": "raw" if is_pdf else "auto",
            "access_mode": "public",
            "overwrite": True,
        }

        # 3. Forzar el public_id con el nombre limpio
        if is_pdf:
            upload_kwargs["public_id"] = f"{clean_name}.pdf"
        else:
            upload_kwargs["public_id"] = clean_name

        result = await asyncio.to_thread(cloudinary.uploader.upload, contents, **upload_kwargs)

        secure_url = result.get("secure_url")
        if not secure_url:
            raise HTTPException(status_code=500, detail="Error al obtener URL de Cloudinary")

        # ✨ TRUCO DINÁMICO: Inyectar el flag de descarga en la URL
        # Esto le dice a Cloudinary que cuando alguien haga clic, el archivo
        # se descargue con el nombre que definimos en clean_name.
        if is_pdf:
            # Reemplazamos /upload/ por /upload/fl_attachment:{nombre_limpio}/
            secure_url = secure_url.replace("/upload/", f"/upload/fl_attachment:{clean_name}/")

        return secure_url

    except Exception as e:
        logger.error(f"Fallo en la subida a Cloudinary: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error en el servidor de medios: {str(e)}")
    finally:
        await file.close()