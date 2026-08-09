from app.models.base import Base
from sqlalchemy import Column, Integer, String, Text


class ExperienceSection(Base):
    __tablename__ = "experience_sections"

    id = Column(Integer, primary_key=True, index=True)
    tagline = Column(String, nullable=False, default="Experiencia")
    title = Column(
        Text,
        nullable=False,
        default='Seleccioná tu <span class="text-amber-400">rubro</span>',
    )
    description = Column(
        Text,
        nullable=False,
        default="Tocá tu industria y descubrí lo que construimos para negocios como el tuyo.",
    )
