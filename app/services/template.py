"""Template rendering service using Jinja2"""

from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi.responses import HTMLResponse
from core.config import config
from typing import Dict, Any


class TemplateService:
    """Template rendering service using Jinja2"""

    def __init__(self):
        self.templates = Jinja2Templates(directory=f"{config.APPROOT}{config.TEMPLATES_DIR}")

    def render(
        self,
        request: Request,
        template_name: str,
        context: Dict[str, Any] = None
    ) -> HTMLResponse:
        """
        Render template with context

        Args:
            request: FastAPI request object
            template_name: Template file name
            context: Context variables for template

        Returns:
            HTML response
        """
        ctx = context or {}

        # Add common context variables
        ctx.update({
            "request": request,
            "_baseurl": config.APP_URL,
            "app_url": config.APP_URL,
            "asset_url": config.ASSET_URL,
            "user": request.state.user if hasattr(request.state, "user") else None
        })

        # Ensure .html extension
        if not template_name.endswith(".html"):
            template_name = f"{template_name}.html"

        return self.templates.TemplateResponse(template_name, ctx)
