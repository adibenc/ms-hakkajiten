"""Authentication API routes"""

from fastapi import APIRouter, Request, Depends, Form
from sqlalchemy.ext.asyncio import AsyncSession
from core.di import injector
from core.database import get_db
from app.controllers.auth import AuthController, LoginRequest, RegisterRequest, PasswordResetRequest, PasswordChangeRequest

auth_router = APIRouter()


# Login routes
@auth_router.get("/login")
async def show_login(
    request: Request,
    controller: AuthController = Depends(lambda: injector.get(AuthController))
):
    """Show login page"""
    return controller.show_login(request)


@auth_router.post("/login")
async def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: AsyncSession = Depends(get_db),
    controller: AuthController = Depends(lambda: injector.get(AuthController))
):
    """Process login"""
    data = LoginRequest(username=username, password=password)
    return await controller.login(request, db, data)


@auth_router.get("/logout")
async def logout(
    request: Request,
    controller: AuthController = Depends(lambda: injector.get(AuthController))
):
    """Logout"""
    return await controller.logout(request)


# Register routes
@auth_router.get("/register")
async def show_register(
    request: Request,
    controller: AuthController = Depends(lambda: injector.get(AuthController))
):
    """Show registration page"""
    return controller.show_register(request)


@auth_router.post("/register")
async def register(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    password_confirmation: str = Form(...),
    phone: str = Form(None),
    db: AsyncSession = Depends(get_db),
    controller: AuthController = Depends(lambda: injector.get(AuthController))
):
    """Process registration"""
    data = RegisterRequest(
        name=name,
        email=email,
        password=password,
        password_confirmation=password_confirmation,
        phone=phone
    )
    return await controller.register(request, db, data)


# Password reset routes
@auth_router.get("/password/email")
async def show_password_reset(
    request: Request,
    controller: AuthController = Depends(lambda: injector.get(AuthController))
):
    """Show password reset request page"""
    return controller.show_password_reset(request)


@auth_router.post("/password/email")
async def request_password_reset(
    request: Request,
    email: str = Form(...),
    db: AsyncSession = Depends(get_db),
    controller: AuthController = Depends(lambda: injector.get(AuthController))
):
    """Request password reset"""
    data = PasswordResetRequest(email=email)
    return await controller.request_password_reset(request, db, data)


@auth_router.get("/password/reset")
async def show_change_password(
    request: Request,
    token: str,
    controller: AuthController = Depends(lambda: injector.get(AuthController))
):
    """Show password change page"""
    return controller.show_change_password(request, token)


@auth_router.post("/password/reset")
async def change_password(
    request: Request,
    password: str = Form(...),
    password_confirmation: str = Form(...),
    token: str = Form(...),
    db: AsyncSession = Depends(get_db),
    controller: AuthController = Depends(lambda: injector.get(AuthController))
):
    """Change password"""
    data = PasswordChangeRequest(
        password=password,
        password_confirmation=password_confirmation,
        token=token
    )
    return await controller.change_password(request, db, data)


# Home route (authenticated)
@auth_router.get("/home")
async def home(
    request: Request,
    controller: AuthController = Depends(lambda: injector.get(AuthController))
):
    """Authenticated home page"""
    # Check auth cookie
    # For now, just render the template
    from app.services.template import TemplateService
    template_service = injector.get(TemplateService)
    return template_service.render(request, "auth/home")
