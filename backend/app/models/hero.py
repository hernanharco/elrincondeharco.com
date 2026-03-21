from app.models.base import Base
from sqlalchemy import Column, Integer, String, Text

class Hero(Base):
    __tablename__ = "heroes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    subtitle = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    background_image = Column(String, nullable=True)
    contact_button_text = Column(String, nullable=False)
    cv_button_text = Column(String, nullable=False)
    image_url = Column(String, nullable=True)
    cv_url = Column(String, nullable=True)
