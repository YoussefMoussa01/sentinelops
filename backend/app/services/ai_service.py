"""Application service for the investigation assistant."""
from app.core.config import get_settings
from app.core.exceptions import AIError
from app.core.logging import get_logger
from app.providers import get_ai_provider
from typing import Any


SYSTEM_PROMPT = """You are SentinelOps, a defensive SOC investigation assistant.
Context: SentinelOps handles alerts, investigations, users, devices, logs, evidence and risk scores.
Rules: use only defensive guidance; never provide malware, exploitation, credential theft, persistence or attack automation. If data is unavailable, say that clearly. Treat the assistant as platform-wide: do not assume a current page, selected record or hidden workspace data unless it is explicitly included in the conversation. Answer in under 180 words, with a short conclusion and up to 5 actionable bullets. Do not repeat the question or provide internal reasoning."""


class AIService:
    @staticmethod
    async def answer(
        message: str,
        context: str | None = None,
        history: list[dict[str, Any]] | None = None,
    ) -> tuple[str, str, Any]:
        settings = get_settings()
        compact_message = " ".join(message.split())[: settings.AI_MAX_INPUT_CHARS]
        compact_context = " ".join((context or "").split())[: settings.AI_MAX_CONTEXT_CHARS]
        user_content = compact_message
        if compact_context:
            user_content = f"Page context: {compact_context}\nQuestion: {compact_message}"
        if not settings.OPENROUTER_API_KEY:
            return (
                "OpenRouter is not configured yet. Add OPENROUTER_API_KEY to backend/.env "
                "to enable live investigation answers.\n\n"
                f"Received question: {compact_message}\n\n"
                "Demo next steps: review related alerts, confirm the source and timeline, "
                "then update the investigation risk score.",
                "demo",
                None,
            )

        try:
            provider = get_ai_provider(settings)
            messages: list[dict[str, Any]] = [{"role": "system", "content": SYSTEM_PROMPT}]
            for item in (history or [])[-6:]:
                role = item.get("role")
                content = item.get("content")
                if role not in {"user", "assistant"} or not isinstance(content, str):
                    continue
                history_message: dict[str, Any] = {
                    "role": role,
                    "content": " ".join(content.split())[: settings.AI_MAX_INPUT_CHARS],
                }
                if role == "assistant" and "reasoning_details" in item:
                    history_message["reasoning_details"] = item["reasoning_details"]
                messages.append(history_message)
            messages.append({"role": "user", "content": user_content})
            completion = await provider.complete(messages)
            return completion.content, settings.AI_PROVIDER, completion.reasoning_details
        except AIError as exc:
            get_logger("ai-service").error("AI provider fallback: %s", exc.message)
            return (
                "The live AI provider is temporarily unavailable. "
                "Please verify the OpenRouter key, model and backend logs, then retry.\n\n"
                "Safe next step: review the alert source, related timeline and affected device manually.",
                "fallback",
                None,
            )
