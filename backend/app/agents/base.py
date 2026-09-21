"""Base agent contract for tool-using investigation agents."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from sqlalchemy.orm import Session


class BaseAgent(ABC):
    """A stateful, permission-aware agent that can call authorized tools."""

    def __init__(self, db: Session, user: Any):
        self.db = db
        self.user = user

    @abstractmethod
    async def run(
        self,
        message: str,
        context: str | None = None,
        history: list[dict[str, Any]] | None = None,
        conversation_id: str | None = None,
    ) -> tuple[str, str, Any, list[dict[str, Any]]]:
        """Return (answer, provider_label, reasoning_details, tool_results)."""
        raise NotImplementedError