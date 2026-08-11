from app.models.base import Base
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    image_urls = Column(JSONB, nullable=False, default=list)
    tags = Column(JSONB, nullable=False)
    icon_name = Column(String, nullable=False)
    color = Column(String, nullable=False)
    demo_url = Column(String, nullable=True)
    github_url = Column(String, nullable=True)
