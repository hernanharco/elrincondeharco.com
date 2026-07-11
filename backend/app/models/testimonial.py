from app.models.base import Base
from sqlalchemy import Column, Integer, String, Text, Boolean


class Testimonial(Base):
    __tablename__ = "testimonials"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    role = Column(String, nullable=True)
    company = Column(String, nullable=True)
    content = Column(Text, nullable=False)
    rating = Column(Integer, default=5)
    avatar_url = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    sort_order = Column(Integer, default=0)
