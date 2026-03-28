"""Home API routes"""

from fastapi import APIRouter, Request, Depends
from core.di import injector
from app.controllers.home import HomeController

home_router = APIRouter()


@home_router.get("/")
async def index(
    request: Request,
    controller: HomeController = Depends(lambda: injector.get(HomeController))
):
    """Home page"""
    return controller.index(request)


@home_router.get("/j1")
async def j1(
    controller: HomeController = Depends(lambda: injector.get(HomeController))
):
    """JSON test endpoint"""
    return controller.j1()
