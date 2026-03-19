from app.models.base import Base
from sqlalchemy import Column, Integer, String, Text

class About(Base):
    __tablename__ = "abouts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    image_url = Column(String, nullable=True)
    location = Column(String, nullable=False)
    years_experience = Column(String, nullable=False)
    team_name = Column(String, nullable=False)
    leadership_title = Column(String, nullable=False)
    leadership_desc = Column(Text, nullable=False)
    experience_title = Column(String, nullable=False)
    experience_desc = Column(Text, nullable=False)
