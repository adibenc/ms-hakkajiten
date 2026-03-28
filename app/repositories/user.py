"""User repository for database operations"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.repository import BBaseRepository
from app.models.user import User
from typing import Optional
import bcrypt


class UserRepository(BBaseRepository):
    """User repository for database operations"""

    def __init__(self):
        super().__init__()

    async def find_by_email(self, db: AsyncSession, email: str, include_deleted=False) -> Optional[User]:
        """
        Find user by email

        Args:
            db: Database session
            email: User email
            include_deleted: Include soft-deleted users

        Returns:
            User or None
        """
        query = select(User).where(User.email == email)
        if not include_deleted:
            query = query.where(User.deleted_at.is_(None))

        result = await db.execute(query)
        return result.scalar_one_or_none()

    async def find_by_id(self, db: AsyncSession, user_id: int, include_deleted=False) -> Optional[User]:
        """
        Find user by ID

        Args:
            db: Database session
            user_id: User ID
            include_deleted: Include soft-deleted users

        Returns:
            User or None
        """
        query = select(User).where(User.id == user_id)
        if not include_deleted:
            query = query.where(User.deleted_at.is_(None))

        result = await db.execute(query)
        return result.scalar_one_or_none()

    async def create_user(
        self,
        db: AsyncSession,
        name: str,
        email: str,
        password: str,
        phone: str = None
    ) -> User:
        """
        Create new user with hashed password

        Args:
            db: Database session
            name: User name
            email: User email
            password: Plain text password (will be hashed)
            phone: User phone (optional)

        Returns:
            Created user
        """
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        user = User(
            name=name,
            email=email,
            password=hashed_password,
            phone=phone
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

    async def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verify password against hash

        Args:
            plain_password: Plain text password
            hashed_password: Bcrypt hashed password

        Returns:
            True if password matches
        """
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

    async def update_password(self, db: AsyncSession, user: User, new_password: str):
        """
        Update user password

        Args:
            db: Database session
            user: User object
            new_password: New plain text password
        """
        user.password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        await db.commit()
        await db.refresh(user)

    async def soft_delete_user(self, db: AsyncSession, user: User):
        """
        Soft delete user

        Args:
            db: Database session
            user: User object
        """
        user.soft_delete()
        await db.commit()
