"""Password reset token model"""

from sqlalchemy import Column, String, DateTime, func
from core.database import Base


class PasswordReset(Base):
    """Password reset token model"""
    __tablename__ = "password_resets"

    email = Column(String(255), primary_key=True, unique=True, index=True)
    token = Column(String(255), nullable=False)
    expires_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
