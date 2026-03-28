"""Application configuration using Pydantic BaseSettings"""

from pydantic_settings import BaseSettings
from enum import Enum
from typing import Optional


class EnvironmentType(str, Enum):
    """Environment types"""
    DEVELOPMENT = "development"
    PRODUCTION = "production"
    TEST = "test"


class Config(BaseSettings):
    """Application configuration following fa-pidum pattern"""

    # Environment
    ENVIRONMENT: EnvironmentType = EnvironmentType.DEVELOPMENT
    DEBUG: bool = True

    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    APP_URL: str = "http://localhost:8000"

    # Security
    APP_KEY: str = "-RkDOqXojJIlsF_I8wWiUq_KRZ0PtGWTOZ676u5HtLg="
    JWT_SECRET_KEY: str = "-RkDOqXojJIlsF_I8wWiUq_KRZ0PtGWTOZ676u5HtLg="
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = 24
    JWT_AUDIENCE: str = "ms-hakkajiten"

    # Database (PostgreSQL)
    DB_CONNECTION: str = "postgres"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "hakkajiten"
    DB_USER: str = "postgres"
    DB_PASS: str = "postgres"

    # Application Paths
    APPROOT: str = "/media/data1/project1/ms-hakkajiten/"
    TEMPLATES_DIR: str = "templates"
    STATIC_DIR: str = "static"
    STORAGE_DIR: str = "storage"

    # Email Configuration
    MAIL_DRIVER: str = "terminal"  # smtp, terminal
    MAIL_HOST: str = "smtp.gmail.com"
    MAIL_PORT: int = 587
    MAIL_USERNAME: str = ""
    MAIL_PASSWORD: str = ""
    MAIL_FROM: str = "no-reply@hakkajiten.com"
    MAIL_FROM_NAME: str = "Hakkajiten"

    # Password Reset
    PASSWORD_RESET_EXPIRATION_MINUTES: int = 1440  # 24 hours

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Global config instance
config = Config()
