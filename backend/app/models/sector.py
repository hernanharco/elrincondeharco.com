from app.models.base import Base
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB


class Sector(Base):
    __tablename__ = "sectors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    client_name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    icon_path = Column(String, nullable=False)
    color_gradient = Column(String, nullable=False)
    sort_order = Column(Integer, default=0)
    project_ids = Column(JSONB, default=list)
