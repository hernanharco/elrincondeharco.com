from sqlalchemy import Column, Integer, String, JSON, Boolean
from sqlalchemy.orm import relationship
from app.models.base import Base


class SiteSettings(Base):
    __tablename__ = "site_settings"

    id = Column(Integer, primary_key=True, index=True)
    brand_name = Column(String(100), nullable=False, default="elRincondelHarco.com")
    site_url = Column(String(255), nullable=False, default="https://elrincondelharco.com")
    legal_name = Column(String(255), nullable=False, default="Hernan Arango Cortes")
    slogan = Column(String(500), nullable=True)
    copyright_notice = Column(String(255), nullable=False, default="Todos los derechos reservados.")
    contact_email = Column(String(255), nullable=False)
    social_networks = Column(JSON, nullable=True)
    is_active = Column(Boolean, default=True)
    
    def __repr__(self):
        return f"<SiteSettings(id={self.id}, brand_name='{self.brand_name}')>"
