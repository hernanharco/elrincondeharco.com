from app.models.base import Base
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB

class Footer(Base):
    __tablename__ = "footers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    location = Column(String, nullable=False)
    email = Column(String, nullable=False)
    github_url = Column(String, nullable=True)
    linkedin_url = Column(String, nullable=True)
    twitter_url = Column(String, nullable=True)
    quick_links = Column(JSONB, nullable=False)
