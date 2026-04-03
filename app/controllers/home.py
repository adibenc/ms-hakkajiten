"""Home controller"""

from injector import inject
from fastapi import Request
from core.controller import BBaseController
from app.services.template import TemplateService
from core.config import config

class HomeController(BBaseController):
    """Home controller"""

    @inject
    def __init__(self, template_service: TemplateService):
        super().__init__()
        self.template_service = template_service

    def index(self, request: Request):
        """
        Render home/welcome page

        Args:
            request: FastAPI request object

        Returns:
            HTML response
        """
        return self.template_service.render(request, "welcome")

    def j1(self):
        """
        JSON API test endpoint

        Returns:
            JSON response with test data
        """
        return self.success("Ok", {"d1": 1337, **dict(config)})
