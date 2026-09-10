"""AI provider factory."""
from app.core.config import Settings
from app.core.exceptions import AIError
from app.providers.base import AIProvider
from app.providers.openrouter import OpenRouterProvider


def get_ai_provider(settings: Settings) -> AIProvider:
    if settings.AI_PROVIDER.lower() == "openrouter":
        return OpenRouterProvider(settings)
    raise AIError(f"Unsupported AI provider: {settings.AI_PROVIDER}")


__all__ = ["AIProvider", "OpenRouterProvider", "get_ai_provider"]
