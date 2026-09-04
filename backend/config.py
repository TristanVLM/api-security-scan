from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """ Application settings loaded from environment variables or a .env file.
    """

    model_config = SettingsConfigDict(env_file="../.env", env_file_encoding="utf-8", case_sensitive=True)

    # Application metadata
    APP_NAME: str = "API Security Scan"
    VERSION: str = "1.0.0"
    DEBUG: bool = False

    # Database configuration
    DATABASE_URL: str = "postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}"
    POSTGRES_USER: str = "apiuser"
    POSTGRES_PASSWORD: str = "apipass"
    POSTGRES_DB: str = "apisecurity"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432

    # Security
    SECRET_KEY: str = "your-secret-key"  # Replace with a secure
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours

    # Backend server
    BACKEND_HOST: str = "0.0.0.0"
    BACKEND_PORT: int = 8000

    # Field validation constraints
    PASSWORD_MIN_LENGTH: int = 8
    PASSWORD_MAX_LENGTH: int = 100
    EMAIL_MAX_LENGTH: int = 255

    # Default maximum requests for scans
    DEFAULT_MAX_REQUESTS : int = 100
    DEFAULT_TIMEOUT_SECONDS: int = 10
    DEFAULT_RETRY_COUNT: int = 3

    # Scanner timeout and connection limits
    SCANNER_CONNECTION_TIMEOUT: int = 30

    # Scanner rate limiting
    SCANNER_RATE_LIMIT_WINDOW_SECONDS: int = 60

    # Scanner request spacing and timing
    DEFAULT_JITTER_MS: int = 100
    DEFAULT_RETRY_WAIT_SECONDS: int = 60



@lru_cache
def get_settings() -> Settings:
    """Get the application settings."""
    return Settings()

settings = get_settings()