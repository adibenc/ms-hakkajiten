"""Dependency injection container"""

from injector import Injector
from core.app_module import AppModule


def create_injector() -> Injector:
    """Create and configure the dependency injection container"""
    return Injector([AppModule()])


# Global injector instance
injector = create_injector()
