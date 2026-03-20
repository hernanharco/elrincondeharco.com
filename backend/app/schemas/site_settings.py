from pydantic import BaseModel, Field, HttpUrl, model_validator, ConfigDict
from typing import Optional, Any


class SocialNetworks(BaseModel):
    # Usamos Union con str o validamos cuidadosamente porque 
    # HttpUrl de Pydantic v2 es más estricto que en la v1
    github: Optional[HttpUrl] = None
    linkedin: Optional[HttpUrl] = None
    twitter: Optional[HttpUrl] = None
    instagram: Optional[HttpUrl] = None

    @model_validator(mode='before')
    @classmethod
    def validate_urls_none_string(cls, data: Any) -> Any:
        """Convierte strings 'None' o vacíos en None reales antes de validar la URL."""
        if isinstance(data, dict):
            for field in ['github', 'linkedin', 'twitter', 'instagram']:
                val = data.get(field)
                if val is not None and (str(val).lower() in ["none", "null", ""]):
                    data[field] = None
        return data


class SiteSettingsBase(BaseModel):
    brand_name: str = Field(..., max_length=100)
    site_url: HttpUrl = Field(...)
    legal_name: str = Field(..., max_length=255)
    slogan: Optional[str] = Field(None, max_length=500)
    copyright_notice: str = Field(..., max_length=255)
    contact_email: str = Field(..., max_length=255)
    social_networks: Optional[SocialNetworks] = None
    is_active: Optional[bool] = Field(True)


class SiteSettingsCreate(SiteSettingsBase):
    pass


class SiteSettingsUpdate(BaseModel):
    # En Update, todo es opcional para permitir actualizaciones parciales (PATCH/PUT parcial)
    brand_name: Optional[str] = Field(None, max_length=100)
    site_url: Optional[HttpUrl] = None
    legal_name: Optional[str] = Field(None, max_length=255)
    slogan: Optional[str] = Field(None, max_length=500)
    copyright_notice: Optional[str] = Field(None, max_length=255)
    contact_email: Optional[str] = Field(None, max_length=255)
    social_networks: Optional[SocialNetworks] = None
    is_active: Optional[bool] = None

    @model_validator(mode='before')
    @classmethod
    def handle_none_strings(cls, data: Any) -> Any:
        """Limpia strings traicioneros del FormData en el esquema de actualización."""
        if isinstance(data, dict):
            for key, value in data.items():
                if value is not None and str(value).lower() in ["none", "null", ""]:
                    data[key] = None
        return data


class SiteSettingsResponse(SiteSettingsBase):
    id: int
    
    # Configuración moderna de Pydantic v2 para leer desde SQLAlchemy
    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode='before')
    @classmethod
    def validate_is_active_null(cls, data: Any) -> Any:
        # Aseguramos que is_active nunca sea None al salir hacia el frontend
        if isinstance(data, dict):
            if data.get('is_active') is None:
                data['is_active'] = True
        else:
            if hasattr(data, 'is_active') and data.is_active is None:
                data.is_active = True
        return data