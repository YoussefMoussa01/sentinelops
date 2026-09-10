"""Provider contract for model-backed assistant responses."""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass
class AICompletion:
    content: str
    reasoning_details: Any = None


class AIProvider(ABC):
    @abstractmethod
    async def complete(self, messages: list[dict[str, Any]]) -> AICompletion:
        """Return assistant text and provider continuation metadata."""
        raise NotImplementedError
