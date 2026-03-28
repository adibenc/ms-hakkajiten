"""Wiki controller for serving wiki content"""

from injector import inject
from fastapi import Request
import os
import re
from core.controller import BBaseController
from app.services.template import TemplateService
from app.helpers.common import scan_dir_rc
from core.config import config


class WikiController(BBaseController):
    """Wiki controller for serving wiki content"""

    @inject
    def __init__(self, template_service: TemplateService):
        super().__init__()
        self.template_service = template_service
        self.prename = "wiki"

    def list(self, request: Request):
        """
        List all wiki files

        Args:
            request: FastAPI request object

        Returns:
            HTML response with wiki file list
        """
        try:
            rootdir = config.APPROOT
            fname = f"{rootdir}{config.TEMPLATES_DIR}/{self.prename}"

            list_of_files = scan_dir_rc(fname)
            # Remove .html and .php extensions
            list_of_files = [re.sub(r'(\.html$|\.php$)', '', x) for x in list_of_files]

            # Filter out 'dmy' files (requires auth middleware in Masonite)
            list_of_files = [x for x in list_of_files if "dmy" not in x]

            return self.template_service.render(
                request,
                f"{self.prename}/list",
                {
                    "prename": self.prename,
                    "files": list_of_files
                }
            )
        except Exception as e:
            return self.fail(str(e), [1])

    def d(self, request: Request, f: str = None):
        """
        Serve single wiki file

        Args:
            request: FastAPI request object
            f: File name

        Returns:
            HTML response with wiki content
        """
        try:
            f = f or "f3-bio"
            return self.template_service.render(request, f"{self.prename}/{f}")
        except Exception as e:
            return self.fail(str(e), [1])

    def dc(self, request: Request, c: str = None, c1: str = None, c2: str = None, f: str = None):
        """
        Serve categorized wiki file (2-3 level hierarchy)

        Args:
            request: FastAPI request object
            c: Category (2-level)
            c1: Category 1 (3-level)
            c2: Category 2 (3-level)
            f: File name

        Returns:
            HTML response with wiki content
        """
        try:
            f = f or "f3-bio"

            # 2-level: wiki/c/{category}/{file}
            if c and f and not c1:
                return self.template_service.render(request, f"{self.prename}/{c}/{f}")

            # 3-level: wiki/c/{cat1}/{cat2}/{file}
            if c1 and c2 and f:
                return self.template_service.render(request, f"{self.prename}/{c1}/{c2}/{f}")

            return self.fail("Invalid wiki path", None)
        except Exception as e:
            return self.fail(str(e), [1])
