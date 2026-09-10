"""OpenRouter chat-completions provider."""
import asyncio
import httpx
from typing import Any
from app.core.logging import get_logger

from app.core.config import Settings
from app.core.exceptions import AIError
from app.providers.base import AICompletion, AIProvider


class OpenRouterProvider(AIProvider):
    endpoint = "https://openrouter.ai/api/v1/chat/completions"

    def __init__(self, settings: Settings):
        self.settings = settings
        self.logger = get_logger("openrouter")

    async def complete(self, messages: list[dict[str, Any]]) -> AICompletion:
        if not self.settings.OPENROUTER_API_KEY:
            raise AIError("OpenRouter is not configured. Set OPENROUTER_API_KEY in backend/.env.")

        headers = {
            "Authorization": f"Bearer {self.settings.OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        }
        if self.settings.AI_SITE_URL:
            headers["HTTP-Referer"] = self.settings.AI_SITE_URL
        if self.settings.AI_SITE_NAME:
            headers["X-OpenRouter-Title"] = self.settings.AI_SITE_NAME

        payload = {
            "model": self.settings.AI_MODEL,
            "messages": messages,
            "temperature": self.settings.AI_TEMPERATURE,
            "max_tokens": self.settings.AI_MAX_TOKENS,
            "reasoning": {"enabled": self.settings.AI_REASONING_ENABLED},
        }
        fallback_models = [
            model.strip()
            for model in self.settings.AI_FALLBACK_MODELS.split(",")
            if model.strip() and model.strip() != self.settings.AI_MODEL
        ]
        if fallback_models:
            payload["models"] = fallback_models
            self.logger.info(
                "OpenRouter fallback models configured: %s",
                ", ".join(fallback_models),
            )

        retryable_statuses = {429, 500, 502, 503, 504}
        max_attempts = max(0, self.settings.AI_RETRY_ATTEMPTS)

        async with httpx.AsyncClient(timeout=self.settings.AI_TIMEOUT_SECONDS) as client:
            for attempt in range(max_attempts + 1):
                try:
                    response = await client.post(self.endpoint, headers=headers, json=payload)
                    response.raise_for_status()
                    data = response.json()
                    break
                except httpx.HTTPStatusError as exc:
                    status = exc.response.status_code
                    self.logger.error(
                        "OpenRouter rejected completion: status=%s attempt=%s/%s body=%s",
                        status,
                        attempt + 1,
                        max_attempts + 1,
                        exc.response.text[:500],
                    )
                    if status not in retryable_statuses or attempt >= max_attempts:
                        raise AIError(f"OpenRouter request failed with status {status}.") from exc

                    retry_after = exc.response.headers.get("Retry-After")
                    try:
                        delay = float(retry_after) if retry_after else 0.0
                    except ValueError:
                        delay = 0.0
                    delay = min(
                        max(delay, self.settings.AI_RETRY_BACKOFF_SECONDS * (2**attempt)),
                        10.0,
                    )
                    self.logger.warning(
                        "Retrying OpenRouter request in %.1fs after status %s",
                        delay,
                        status,
                    )
                    await asyncio.sleep(delay)
                except httpx.RequestError as exc:
                    self.logger.error(
                        "OpenRouter transport error: %s attempt=%s/%s",
                        type(exc).__name__,
                        attempt + 1,
                        max_attempts + 1,
                    )
                    if attempt >= max_attempts:
                        raise AIError("OpenRouter could not be reached.") from exc
                    delay = min(
                        self.settings.AI_RETRY_BACKOFF_SECONDS * (2**attempt),
                        10.0,
                    )
                    await asyncio.sleep(delay)
                except ValueError as exc:
                    self.logger.error("OpenRouter returned invalid JSON")
                    raise AIError("OpenRouter returned an invalid response.") from exc

        try:
            assistant_message = data["choices"][0]["message"]
            if not isinstance(assistant_message, dict):
                raise TypeError("assistant message is not an object")
            content = assistant_message.get("content")
        except (KeyError, IndexError, TypeError) as exc:
            self.logger.error("OpenRouter returned an unexpected completion shape")
            raise AIError("OpenRouter returned an invalid completion.") from exc

        if isinstance(content, list):
            content = "\n".join(
                part.get("text", "")
                for part in content
                if isinstance(part, dict) and isinstance(part.get("text"), str)
            )

        if not isinstance(content, str) or not content.strip():
            choices = data.get("choices")
            finish_reason = (
                choices[0].get("finish_reason")
                if isinstance(choices, list)
                and choices
                and isinstance(choices[0], dict)
                else None
            )
            self.logger.error(
                "OpenRouter returned empty content: model=%s finish_reason=%s has_reasoning=%s",
                data.get("model"),
                finish_reason,
                bool(assistant_message.get("reasoning_details")),
            )
            raise AIError("OpenRouter returned an empty completion.")
        return AICompletion(
            content=content.strip(),
            reasoning_details=assistant_message.get("reasoning_details"),
        )
