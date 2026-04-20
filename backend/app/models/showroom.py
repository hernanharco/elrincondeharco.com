from app.models.base import Base
from sqlalchemy import Column, Integer, String, Text

class Showroom(Base):
    __tablename__ = "showroom"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String, nullable=False)
    deploy_url = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
