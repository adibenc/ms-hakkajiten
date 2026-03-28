"""JWT Authentication module following fa-pidum pattern"""

import jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status, Request, Response
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from core.config import config

security = HTTPBearer(auto_error=False)


def create_access_token(user_id: int, email: str) -> str:
    """
    Create JWT access token

    Args:
        user_id: User ID
        email: User email

    Returns:
        JWT token string
    """
    payload = {
        "user_id": user_id,
        "email": email,
        "exp": datetime.utcnow() + timedelta(hours=config.JWT_EXPIRATION_HOURS),
        "iat": datetime.utcnow(),
        "aud": config.JWT_AUDIENCE
    }
    return jwt.encode(payload, config.JWT_SECRET_KEY, algorithm=config.JWT_ALGORITHM)


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """
    Verify JWT token from Authorization header

    Args:
        credentials: HTTP Bearer credentials

    Returns:
        Token payload dict

    Raises:
        HTTPException: 401 if token invalid/expired
    """
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authentication token"
        )

    token = credentials.credentials
    try:
        payload = jwt.decode(
            token,
            config.JWT_SECRET_KEY,
            algorithms=[config.JWT_ALGORITHM],
            audience=config.JWT_AUDIENCE
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )


async def get_current_user_optional(request: Request) -> Optional[dict]:
    """
    Get current user from JWT token in HTTP-only cookie OR Authorization header
    Returns None if not authenticated (no exception)

    Args:
        request: FastAPI request object

    Returns:
        User payload dict or None
    """
    # Try JWT from cookie first (for template rendering)
    token = request.cookies.get("access_token")

    # Try Authorization header if no cookie
    if not token:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.replace("Bearer ", "")

    if not token:
        return None

    try:
        payload = jwt.decode(
            token,
            config.JWT_SECRET_KEY,
            algorithms=[config.JWT_ALGORITHM],
            audience=config.JWT_AUDIENCE
        )
        return payload
    except:
        return None


async def get_current_user(request: Request) -> dict:
    """
    Get current user - REQUIRED (raises exception if not authenticated)

    Args:
        request: FastAPI request object

    Returns:
        User payload dict

    Raises:
        HTTPException: 401 if not authenticated
    """
    user = await get_current_user_optional(request)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    return user


def set_auth_cookie(response: Response, token: str):
    """
    Set JWT token in HTTP-only cookie

    Args:
        response: FastAPI response object
        token: JWT token string
    """
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        max_age=config.JWT_EXPIRATION_HOURS * 3600,  # Convert hours to seconds
        samesite="lax",
        secure=config.ENVIRONMENT == "production"
    )


def clear_auth_cookie(response: Response):
    """
    Clear JWT cookie (for logout)

    Args:
        response: FastAPI response object
    """
    response.delete_cookie(key="access_token")
