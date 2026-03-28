"""Dependency injection module configuration following fa-pidum pattern"""

from injector import Module, singleton, Binder


class AppModule(Module):
    """Dependency injection module configuration"""

    def configure(self, binder: Binder):
        """Configure dependency injection bindings"""
        # Import repositories
        from app.repositories.user import UserRepository
        from app.repositories.password_reset import PasswordResetRepository
        from app.repositories.article import ArticleRepository

        # Import services
        from app.services.email import EmailService
        from app.services.template import TemplateService
        from app.services.auth import AuthService

        # Import controllers
        from app.controllers.home import HomeController
        from app.controllers.auth import AuthController
        from app.controllers.wiki import WikiController

        # Repository bindings (singleton scope - shared instance)
        binder.bind(UserRepository, scope=singleton)
        binder.bind(PasswordResetRepository, scope=singleton)
        binder.bind(ArticleRepository, scope=singleton)

        # Service bindings (singleton scope)
        binder.bind(EmailService, scope=singleton)
        binder.bind(TemplateService, scope=singleton)
        binder.bind(AuthService, scope=singleton)

        # Controller bindings (per-request scope)
        binder.bind(HomeController)
        binder.bind(AuthController)
        binder.bind(WikiController)
