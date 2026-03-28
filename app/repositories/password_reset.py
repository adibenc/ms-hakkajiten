"""Password reset repository"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from core.repository import BBaseRepository
from app.models.password_reset import PasswordReset
from typing import Optional
from datetime import datetime, timedelta
import secrets


class PasswordResetRepository(BBaseRepository):
    """Password reset repository"""

    def __init__(self):
        super().__init__()

    async def create_reset_token(
        self,
        db: AsyncSession,
        email: str,
        expiration_minutes: int = 1440
    ) -> str:
        """
        Create password reset token

        Args:
            db: Database session
            email: User email
            expiration_minutes: Token expiration in minutes

        Returns:
            Generated token
        """
        # Generate secure token
        token = secrets.token_urlsafe(32)
        expires_at = datetime.utcnow() + timedelta(minutes=expiration_minutes)

        # Delete existing tokens for this email
        await db.execute(delete(PasswordReset).where(PasswordReset.email == email))

        # Create new token
        reset = PasswordReset(
            email=email,
            token=token,
            expires_at=expires_at
        )
        db.add(reset)
        await db.commit()
        return token

    async def verify_token(self, db: AsyncSession, token: str) -> Optional[str]:
        """
        Verify reset token and return email if valid

        Args:
            db: Database session
            token: Reset token

        Returns:
            Email if token valid, None otherwise
        """
        query = select(PasswordReset).where(PasswordReset.token == token)
        result = await db.execute(query)
        reset = result.scalar_one_or_none()

        if not reset:
            return None

        # Check expiration
        if reset.expires_at and reset.expires_at < datetime.utcnow():
            await db.execute(delete(PasswordReset).where(PasswordReset.token == token))
            await db.commit()
            return None

        return reset.email

    async def delete_token(self, db: AsyncSession, email: str):
        """
        Delete reset token after use

        Args:
            db: Database session
            email: User email
        """
        await db.execute(delete(PasswordReset).where(PasswordReset.email == email))
        await db.commit()
