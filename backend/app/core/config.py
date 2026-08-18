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

    # API
    API_V1_PREFIX: str = "/api/v1"
    API_TITLE: str = "SentinelOps API"
    API_VERSION: str = "0.1.0"

    # CORS
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000"

    # AI
    AI_PROVIDER: str = "openrouter"
    OPENROUTER_API_KEY: str = ""
    AI_MODEL: str = "openai/gpt-4"
    AI_TEMPERATURE: float = 0.7
    AI_MAX_TOKENS: int = 2000

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/sentinelops.log"

    # Security
    ALLOWED_HOSTS: str = "localhost,127.0.0.1"
    DEBUG: bool = False

    # Environment
    ENVIRONMENT: str = "development"

    class Config:
        env_file = ".env"
        case_sensitive = True

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
