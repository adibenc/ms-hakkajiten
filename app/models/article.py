"""Article model (placeholder for future expansion)"""

from sqlalchemy import Column, Integer, String, Text, DateTime, func
from core.database import Base


class Article(Base):
    """Article model (placeholder for future expansion)"""
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=True)
    content = Column(Text, nullable=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
