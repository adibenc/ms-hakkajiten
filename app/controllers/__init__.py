# Legacy Masonite controllers (can be removed after migration)
# from .BaseController import BaseController
# from .ArtController import ArtController

# New FastAPI controllers
from .home import HomeController
from .auth import AuthController
from .wiki import WikiController

__all__ = ["HomeController", "AuthController", "WikiController"]