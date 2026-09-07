"""Investigation assistant API."""
from fastapi import APIRouter
from pydantic import BaseModel, Field
from fastapi import Depends
from app.api.dependencies import check_permission

router = APIRouter(prefix="/ai", tags=["ai"])


class AssistantRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)


@router.post("/query", response_model=dict, dependencies=[Depends(check_permission("use_ai_agent"))])
async def query_assistant(request: AssistantRequest):
    """Return a deterministic first-pass triage response."""
    message = request.message.strip()
    return {
        "answer": (
            f"Received investigation question: {message}\n\n"
            "Next steps: review related alerts, confirm the source and timeline, "
            "then update the investigation risk score."
        ),
        "mode": "triage-assistant",
    }