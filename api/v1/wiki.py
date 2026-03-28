"""Wiki API routes"""

from fastapi import APIRouter, Request, Depends
from core.di import injector
from app.controllers.wiki import WikiController

wiki_router = APIRouter()


@wiki_router.get("/")
async def wiki_list(
    request: Request,
    controller: WikiController = Depends(lambda: injector.get(WikiController))
):
    """List all wiki files"""
    return controller.list(request)


@wiki_router.get("/list")
async def wiki_list_alt(
    request: Request,
    controller: WikiController = Depends(lambda: injector.get(WikiController))
):
    """List all wiki files (alternate route)"""
    return controller.list(request)


@wiki_router.get("/d/{f}")
async def wiki_file(
    request: Request,
    f: str,
    controller: WikiController = Depends(lambda: injector.get(WikiController))
):
    """Serve single wiki file"""
    return controller.d(request, f)


@wiki_router.get("/c/{c}/{f}")
async def wiki_categorized_2level(
    request: Request,
    c: str,
    f: str,
    controller: WikiController = Depends(lambda: injector.get(WikiController))
):
    """Serve wiki file in 2-level category"""
    return controller.dc(request, c=c, f=f)


@wiki_router.get("/c/{c1}/{c2}/{f}")
async def wiki_categorized_3level(
    request: Request,
    c1: str,
    c2: str,
    f: str,
    controller: WikiController = Depends(lambda: injector.get(WikiController))
):
    """Serve wiki file in 3-level category"""
    return controller.dc(request, c1=c1, c2=c2, f=f)
