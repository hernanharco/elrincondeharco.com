from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, Dict, Any


class SocialNetworks(BaseModel):
    github: Optional[HttpUrl] = None
    linkedin: Optional[HttpUrl] = None
    twitter: Optional[HttpUrl] = None


class SiteSettingsBase(BaseModel):
    brand_name: str = Field(..., max_length=100, description="Nombre de la marca/brand")
    site_url: HttpUrl = Field(..., description="URL principal del sitio")
    legal_name: str = Field(..., max_length=255, description="Nombre legal del propietario")
    slogan: Optional[str] = Field(None, max_length=500, description="Slogan o descripción corta")
    copyright_notice: str = Field(..., max_length=255, description="Texto de copyright")
    contact_email: str = Field(..., max_length=255, description="Email de contacto principal")
    social_networks: Optional[SocialNetworks] = Field(None, description="Redes sociales")
    is_active: bool = Field(True, description="Si la configuración está activa")


class SiteSettingsCreate(SiteSettingsBase):
    pass


class SiteSettingsUpdate(BaseModel):
    brand_name: Optional[str] = Field(None, max_length=100)
    site_url: Optional[HttpUrl] = None
    legal_name: Optional[str] = Field(None, max_length=255)
    slogan: Optional[str] = Field(None, max_length=500)
    copyright_notice: Optional[str] = Field(None, max_length=255)
    contact_email: Optional[str] = Field(None, max_length=255)
    social_networks: Optional[SocialNetworks] = None
    is_active: Optional[bool] = None


class SiteSettingsResponse(SiteSettingsBase):
    id: int
    
    class Config:
        from_attributes = True
