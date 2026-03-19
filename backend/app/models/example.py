from sqlalchemy import Column, Integer, String, DateTime, func
from app.models.base import Base


class Example(Base):
    __tablename__ = "examples"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<Example(id={self.id}, name='{self.name}')>"
