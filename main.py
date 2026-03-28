"""FastAPI application entry point"""

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from starlette.middleware.sessions import SessionMiddleware

from api import router as api_router
from core.config import config


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager - handles startup/shutdown tasks"""
    print(f"✓ Environment: {config.ENVIRONMENT}")
    print(f"✓ Database: {config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}")
    print(f"✓ Templates: {config.TEMPLATES_DIR}")
    print(f"✓ Server: {config.HOST}:{config.PORT}")

    yield

    print("✓ Shutdown complete")


def create_app() -> FastAPI:
    """Create and configure FastAPI application"""
    app = FastAPI(
        title="MS Hakkajiten",
        description="Wiki and Knowledge Base System (FastAPI Migration)",
        version="2.0.0",
        lifespan=lifespan,
        docs_url="/docs" if config.ENVIRONMENT.value == "development" else None,
        redoc_url="/redoc" if config.ENVIRONMENT.value == "development" else None,
    )

    # Session middleware (for backward compatibility during migration)
    # Stores JWT tokens in HTTP-only cookies
    app.add_middleware(
        SessionMiddleware,
        secret_key=config.APP_KEY,
        session_cookie="hakkajiten_session",
        max_age=3600 * 24 * 7  # 7 days
    )

    # Mount static files
    try:
        app.mount("/static", StaticFiles(directory=f"{config.APPROOT}{config.STATIC_DIR}"), name="static")
    except:
        print("⚠ Warning: Static directory not found, skipping static file mounting")

    try:
        app.mount("/storage", StaticFiles(directory=f"{config.APPROOT}{config.STORAGE_DIR}"), name="storage")
    except:
        print("⚠ Warning: Storage directory not found, skipping storage file mounting")

    # Register API routers
    app.include_router(api_router)

    # Health check endpoint
    @app.get("/health")
    async def health():
        return {
            "status": "healthy",
            "service": "MS Hakkajiten",
            "version": "2.0.0",
            "environment": config.ENVIRONMENT.value
        }

    return app


# Create application instance
app = create_app()


if __name__ == "__main__":
    # Development server
    uvicorn.run(
        "main:app",
        host=config.HOST,
        port=config.PORT,
        reload=True if config.ENVIRONMENT.value == "development" else False,
        log_level="info"
    )
