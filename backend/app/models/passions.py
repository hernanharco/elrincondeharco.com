from app.models.base import Base
from sqlalchemy import Column, Integer, String, Text

class Passion(Base):
    __tablename__ = "passions"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    image_url = Column(String, nullable=True)
    family_title = Column(String, nullable=False)
    family_desc = Column(Text, nullable=False)
    games_title = Column(String, nullable=False)
    games_desc = Column(Text, nullable=False)
    coding_title = Column(String, nullable=False)
    coding_desc = Column(Text, nullable=False)
