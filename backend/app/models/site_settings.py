from sqlalchemy import Column, Integer, String, JSON, Boolean, Text, text
from sqlalchemy.dialects.postgresql import JSONB
from app.models.base import Base


class SiteSettings(Base):
    __tablename__ = "site_settings"

    id = Column(Integer, primary_key=True, index=True)
    brand_name = Column(String(100), nullable=False, default="elRincondelHarco.com")
    site_url = Column(
        String(255), nullable=False, default="https://elrincondelharco.com"
    )
    legal_name = Column(String(255), nullable=False, default="Hernan Arango Cortes")
    slogan = Column(String(500), nullable=True)
    copyright_notice = Column(
        String(255), nullable=False, default="Todos los derechos reservados."
    )
    contact_email = Column(String(255), nullable=False)

    social_networks = Column(JSON, nullable=True)

    is_active = Column(
        Boolean, default=True, server_default=text("true"), nullable=False
    )

    # ── CTA Section ────────────────────────────────────────────
    cta_title = Column(
        Text,
        nullable=True,
        default='¿Listo para construir <span class="text-amber-400">algo grande</span>?',
    )
    cta_description = Column(
        Text,
        nullable=True,
        default=(
            "Tenés la idea, yo tengo la experiencia para hacerla realidad.\n"
            "Trabajemos juntos para crear una solución que marque la diferencia."
        ),
    )
    cta_features = Column(JSONB, nullable=True, default=list)
    cta_primary_text = Column(String(100), nullable=True, default="Enviar Correo")
    cta_secondary_text = Column(String(100), nullable=True, default="LinkedIn")

    def __repr__(self):
        return f"<SiteSettings(id={self.id}, brand_name='{self.brand_name}')>"
