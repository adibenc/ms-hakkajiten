"""Authentication service layer"""

from injector import inject
from app.repositories.user import UserRepository
from app.repositories.password_reset import PasswordResetRepository
from app.services.email import EmailService
from core.auth import create_access_token
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, Tuple


class AuthService:
    """Authentication service layer"""

    @inject
    def __init__(
        self,
        user_repo: UserRepository,
        password_reset_repo: PasswordResetRepository,
        email_service: EmailService
    ):
        self.user_repo = user_repo
        self.password_reset_repo = password_reset_repo
        self.email_service = email_service

    async def authenticate(self, db: AsyncSession, email: str, password: str) -> Optional[dict]:
        """
        Authenticate user and return JWT token

        Args:
            db: Database session
            email: User email
            password: Plain text password

        Returns:
            Dict with token and user data, or None if authentication failed
        """
        user = await self.user_repo.find_by_email(db, email)

        if not user:
            return None

        # Verify password
        if not await self.user_repo.verify_password(password, user.password):
            return None

        # Create JWT token
        token = create_access_token(user.id, user.email)

        return {
            "token": token,
            "user": user.to_dict()
        }

    async def register(
        self,
        db: AsyncSession,
        name: str,
        email: str,
        password: str,
        phone: str = None
    ) -> dict:
        """
        Register new user

        Args:
            db: Database session
            name: User name
            email: User email
            password: Plain text password
            phone: User phone (optional)

        Returns:
            Dict with token and user data

        Raises:
            ValueError: If email already registered
        """
        # Check if user exists
        existing = await self.user_repo.find_by_email(db, email)
        if existing:
            raise ValueError("Email already registered")

        # Create user
        user = await self.user_repo.create_user(db, name, email, password, phone)

        # Create JWT token
        token = create_access_token(user.id, user.email)

        return {
            "token": token,
            "user": user.to_dict()
        }

    async def request_password_reset(self, db: AsyncSession, email: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Request password reset - returns (email, token)

        Args:
            db: Database session
            email: User email

        Returns:
            Tuple of (email, token) if user exists, (None, None) otherwise
        """
        # Check if user exists
        user = await self.user_repo.find_by_email(db, email)
        if not user:
            # Return dummy values to prevent email enumeration
            return None, None

        # Create reset token
        token = await self.password_reset_repo.create_reset_token(db, email)

        # Send email
        await self.email_service.send_password_reset(email, token)

        return email, token

    async def reset_password(self, db: AsyncSession, token: str, new_password: str) -> bool:
        """
        Reset password using token

        Args:
            db: Database session
            token: Password reset token
            new_password: New plain text password

        Returns:
            True if password reset successful
        """
        # Verify token
        email = await self.password_reset_repo.verify_token(db, token)
        if not email:
            return False

        # Get user
        user = await self.user_repo.find_by_email(db, email)
        if not user:
            return False

        # Update password
        await self.user_repo.update_password(db, user, new_password)

        # Delete token
        await self.password_reset_repo.delete_token(db, email)

        return True
