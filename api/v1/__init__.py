"""API v1 package"""

from fastapi import APIRouter
from .auth import auth_router
from .wiki import wiki_router
from .home import home_router

v1_router = APIRouter()

# Register routers
v1_router.include_router(auth_router, tags=["Authentication"])
v1_router.include_router(wiki_router, prefix="/wiki", tags=["Wiki"])
v1_router.include_router(home_router, tags=["Home"])

__all__ = ["v1_router"]
