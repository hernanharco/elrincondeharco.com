from app.models.base import Base
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB

class Stack(Base):
    __tablename__ = "stacks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    icon = Column(String, nullable=False)
    description = Column(String, nullable=False)
    color = Column(String, nullable=False)
    border = Column(String, nullable=False)
    glow = Column(String, nullable=False)
