"""Investigation assistant API."""
from fastapi import APIRouter
from typing import Any, Literal
from pydantic import BaseModel, Field
from fastapi import Depends
from app.api.dependencies import check_permission
from app.services.ai_service import AIService

router = APIRouter(prefix="/ai", tags=["ai"])


class AssistantRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
    context: str | None = Field(default=None, max_length=1000)
    history: list[dict[str, Any]] = Field(default_factory=list, max_length=8)


@router.post("/query", response_model=dict, dependencies=[Depends(check_permission("use_ai_agent"))])
async def query_assistant(request: AssistantRequest):
    """Return a provider-backed investigation response."""
    message = request.message.strip()
    answer, provider, reasoning_details = await AIService.answer(
        message, request.context, request.history
    )
    return {
        "answer": answer,
        "provider": provider,
        "mode": "triage-assistant",
        "reasoning_details": reasoning_details,
    }
