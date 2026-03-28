"""User model with soft deletes support"""

from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.ext.hybrid import hybrid_property
from core.database import Base
from datetime import datetime


class User(Base):
    """User model matching the existing database schema"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)  # bcrypt hashed
    remember_token = Column(String(100), nullable=True)
    phone = Column(String(20), nullable=True)
    verified_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    deleted_at = Column(DateTime, nullable=True)  # Soft delete

    @hybrid_property
    def is_deleted(self):
        """Check if user is soft-deleted"""
        return self.deleted_at is not None

    def soft_delete(self):
        """Soft delete the user"""
        self.deleted_at = datetime.utcnow()

    def restore(self):
        """Restore a soft-deleted user"""
        self.deleted_at = None

    def to_dict(self, exclude_password=True):
        """
        Convert to dictionary (exclude sensitive fields)

        Args:
            exclude_password: Whether to exclude password from dict

        Returns:
            Dictionary representation of user
        """
        data = {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "verified_at": self.verified_at.isoformat() if self.verified_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
        if not exclude_password:
            data["password"] = self.password
        return data
