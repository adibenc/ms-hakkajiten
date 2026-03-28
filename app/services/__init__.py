"""Service package"""

from .email import EmailService
from .template import TemplateService
from .auth import AuthService

__all__ = ["EmailService", "TemplateService", "AuthService"]
