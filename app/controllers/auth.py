"""Authentication controller"""

from injector import inject
from fastapi import Request, Response
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, EmailStr, field_validator
import re

from core.controller import BBaseController
from app.services.auth import AuthService
from app.services.template import TemplateService
from core.auth import set_auth_cookie, clear_auth_cookie


class LoginRequest(BaseModel):
    """Login request model"""
    username: EmailStr  # Actually email (for compatibility with form field name)
    password: str


class RegisterRequest(BaseModel):
    """Registration request model"""
    name: str
    email: EmailStr
    password: str
    password_confirmation: str
    phone: str = None

    @field_validator('password')
    @classmethod
    def password_strength(cls, v):
        """Validate password strength"""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain lowercase letter')
        if not re.search(r'\d', v):
            raise ValueError('Password must contain digit')
        return v

    @field_validator('password_confirmation')
    @classmethod
    def passwords_match(cls, v, info):
        """Validate passwords match"""
        if 'password' in info.data and v != info.data['password']:
            raise ValueError('Passwords do not match')
        return v


class PasswordResetRequest(BaseModel):
    """Password reset request model"""
    email: EmailStr


class PasswordChangeRequest(BaseModel):
    """Password change request model"""
    password: str
    password_confirmation: str
    token: str

    @field_validator('password')
    @classmethod
    def password_strength(cls, v):
        """Validate password strength"""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        return v

    @field_validator('password_confirmation')
    @classmethod
    def passwords_match(cls, v, info):
        """Validate passwords match"""
        if 'password' in info.data and v != info.data['password']:
            raise ValueError('Passwords do not match')
        return v


class AuthController(BBaseController):
    """Authentication controller"""

    @inject
    def __init__(
        self,
        auth_service: AuthService,
        template_service: TemplateService
    ):
        super().__init__()
        self.auth_service = auth_service
        self.template_service = template_service

    # Login views
    def show_login(self, request: Request):
        """Show login page"""
        return self.template_service.render(request, "auth/login")

    async def login(self, request: Request, db: AsyncSession, data: LoginRequest):
        """Process login"""
        result = await self.auth_service.authenticate(db, data.username, data.password)

        if not result:
            # Render login with error
            return self.template_service.render(
                request,
                "auth/login",
                {"errors": ["The email or password is incorrect"]}
            )

        # Set JWT in HTTP-only cookie
        response = RedirectResponse(url="/home", status_code=302)
        set_auth_cookie(response, result["token"])
        return response

    async def logout(self, request: Request):
        """Logout user"""
        response = RedirectResponse(url="/login", status_code=302)
        clear_auth_cookie(response)
        return response

    # Register views
    def show_register(self, request: Request):
        """Show registration page"""
        return self.template_service.render(request, "auth/register")

    async def register(self, request: Request, db: AsyncSession, data: RegisterRequest):
        """Process registration"""
        try:
            result = await self.auth_service.register(
                db,
                data.name,
                data.email,
                data.password,
                data.phone
            )

            # Set JWT in HTTP-only cookie and redirect
            response = RedirectResponse(url="/home", status_code=302)
            set_auth_cookie(response, result["token"])
            return response

        except ValueError as e:
            return self.template_service.render(
                request,
                "auth/register",
                {"errors": [str(e)]}
            )

    # Password reset views
    def show_password_reset(self, request: Request):
        """Show password reset request page"""
        return self.template_service.render(request, "auth/password_reset")

    async def request_password_reset(self, request: Request, db: AsyncSession, data: PasswordResetRequest):
        """Process password reset request"""
        await self.auth_service.request_password_reset(db, data.email)

        # Always show success to prevent email enumeration
        return self.template_service.render(
            request,
            "auth/password_reset",
            {"success": ["Email sent. Please follow the directions in your email to complete your password reset."]}
        )

    def show_change_password(self, request: Request, token: str):
        """Show password change page"""
        return self.template_service.render(
            request,
            "auth/change_password",
            {"token": token}
        )

    async def change_password(self, request: Request, db: AsyncSession, data: PasswordChangeRequest):
        """Process password change"""
        success = await self.auth_service.reset_password(db, data.token, data.password)

        if success:
            return self.template_service.render(
                request,
                "auth/change_password",
                {"success": ["Password Reset Successfully"], "token": data.token}
            )
        else:
            return self.template_service.render(
                request,
                "auth/change_password",
                {"errors": ["Could not reset your password"], "token": data.token}
            )
