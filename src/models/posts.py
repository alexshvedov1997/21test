from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, Text, String
from .base import Base


class Posts(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False, unique=True)
    post_text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
