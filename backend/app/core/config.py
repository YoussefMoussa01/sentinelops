from pydantic import model_validator
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database
    DATABASE_URL: str = "postgresql://sentinelops:sentinelops_pass@localhost:5432/sentinelops_db"

    # JWT
    JWT_SECRET_KEY: str = "test-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_SECONDS: int = 3600
    JWT_REFRESH_EXPIRATION_SECONDS: int = 604800
    AUTH_RATE_LIMIT_ATTEMPTS: int = 5
    AUTH_RATE_LIMIT_WINDOW_SECONDS: int = 300

    # API
    API_V1_PREFIX: str = "/api/v1"
    API_TITLE: str = "SentinelOps API"
    API_VERSION: str = "0.1.0"

    # CORS
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000"

    # AI
    AI_PROVIDER: str = "openrouter"
    OPENROUTER_API_KEY: str = ""
    AI_MODEL: str = "google/gemma-4-26b-a4b-it:free"
    # Comma-separated OpenRouter model IDs tried after the primary model fails.
    AI_FALLBACK_MODELS: str = ""
    AI_TEMPERATURE: float = 0.7
    AI_MAX_TOKENS: int = 900
    AI_MAX_INPUT_CHARS: int = 1600
    AI_MAX_CONTEXT_CHARS: int = 600
    AI_TIMEOUT_SECONDS: float = 30.0
    AI_RETRY_ATTEMPTS: int = 2
    AI_RETRY_BACKOFF_SECONDS: float = 2.0
    AI_SITE_URL: str = ""
    AI_SITE_NAME: str = "SentinelOps"
    AI_REASONING_ENABLED: bool = False

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/sentinelops.log"

    # Security
    ALLOWED_HOSTS: str = "localhost,127.0.0.1"
    DEBUG: bool = False

    # Environment
    ENVIRONMENT: str = "development"

    # Optional idempotent bootstrap for the first super administrator.
    SUPER_ADMIN_USERNAME: str = ""
    SUPER_ADMIN_EMAIL: str = ""
    SUPER_ADMIN_PASSWORD: str = ""

    class Config:
        env_file = ".env"
        case_sensitive = True

    @model_validator(mode="after")
    def validate_security_settings(self):
        """Reject development defaults when running in production."""
        if self.ENVIRONMENT.lower() == "production":
            if self.DEBUG:
                raise ValueError("DEBUG must be false in production")
            if self.JWT_SECRET_KEY == "test-secret-key-change-in-production" or len(self.JWT_SECRET_KEY) < 32:
                raise ValueError("JWT_SECRET_KEY must be a unique secret of at least 32 characters")
            if not self.CORS_ORIGINS.strip() or "*" in self.CORS_ORIGINS:
                raise ValueError("CORS_ORIGINS must explicitly list trusted origins in production")
            if not self.ALLOWED_HOSTS.strip() or "*" in self.ALLOWED_HOSTS:
                raise ValueError("ALLOWED_HOSTS must explicitly list trusted hosts in production")
        return self

    @property
    def cors_origins_list(self) -> list[str]:
        """Parse CORS origins from comma-separated string."""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

    @property
    def allowed_hosts_list(self) -> list[str]:
        """Parse allowed hosts from comma-separated string."""
        return [host.strip() for host in self.ALLOWED_HOSTS.split(",")]


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
