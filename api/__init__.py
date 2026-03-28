"""API package"""

from fastapi import APIRouter
from .v1 import v1_router

router = APIRouter()

# Mount v1 routes at root (no /v1 prefix for backward compatibility)
router.include_router(v1_router)

__all__ = ["router"]
