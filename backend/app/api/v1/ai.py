"""Investigation assistant API."""
from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse
import json
from time import perf_counter
from typing import Any, Literal
from pydantic import BaseModel, Field
from fastapi import Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.api.dependencies import check_permission, get_current_user
from app.services.ai_service import AIService
from app.services import AuditService, ConversationService
from app.core.exceptions import AppException
from app.tools import SecurityInvestigationTools

router = APIRouter(prefix="/ai", tags=["ai"])


class AssistantRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
    context: str | None = Field(default=None, max_length=1000)
    history: list[dict[str, Any]] = Field(default_factory=list, max_length=8)


class ConversationCreateRequest(BaseModel):
    title: str | None = Field(default=None, max_length=200)


class ConversationMessageRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
    context: str | None = Field(default=None, max_length=1000)


class ConversationUpdateRequest(BaseModel):
    is_archived: bool


class ToolExecutionRequest(BaseModel):
    name: Literal["search_alerts", "search_devices", "search_logs", "inspect_ip"]
    arguments: dict[str, Any] = Field(default_factory=dict)
    conversation_id: str | None = None


class AlertTriageRequest(BaseModel):
    alert_id: str = Field(..., min_length=1, max_length=36)
    conversation_id: str | None = None


class InvestigationBriefRequest(BaseModel):
    investigation_id: str = Field(..., min_length=1, max_length=36)
    conversation_id: str | None = None


def serialize_message(message) -> dict[str, Any]:
    return {
        "id": message.id,
        "role": message.role,
        "content": message.content,
        "provider": message.provider,
        "reasoning_details": message.reasoning_details,
        "created_at": message.created_at.isoformat(),
    }


def serialize_conversation(conversation, include_messages: bool = False) -> dict[str, Any]:
    result: dict[str, Any] = {
        "id": conversation.id,
        "title": conversation.title,
        "is_archived": conversation.is_archived,
        "created_at": conversation.created_at.isoformat(),
        "updated_at": conversation.updated_at.isoformat(),
    }
    if include_messages:
        result["messages"] = [serialize_message(item) for item in conversation.messages]
    return result


def serialize_tool_call(tool_call) -> dict[str, Any]:
    return {
        "id": tool_call.id,
        "tool_name": tool_call.tool_name,
        "arguments": tool_call.arguments,
        "result": tool_call.result,
        "status": tool_call.status,
        "error_message": tool_call.error_message,
        "duration_ms": tool_call.duration_ms,
        "conversation_id": tool_call.conversation_id,
        "created_at": tool_call.created_at.isoformat(),
    }


@router.get("/conversations", response_model=list[dict[str, Any]], dependencies=[Depends(check_permission("use_ai_agent"))])
async def list_conversations(
    include_archived: bool = Query(default=False),
    search: str | None = Query(default=None, max_length=100),
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """List only conversations owned by the authenticated user."""
    return [serialize_conversation(item) for item in ConversationService.list_for_user(db, current_user.id, include_archived, search)]


@router.get("/tool-calls", response_model=list[dict[str, Any]], dependencies=[Depends(check_permission("use_ai_agent"))])
async def list_tool_calls(
    limit: int = Query(default=50, ge=1, le=100),
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Return only the authenticated user's AI tool execution history."""
    return [serialize_tool_call(item) for item in AuditService.list_tool_calls(db, current_user.id, limit)]


@router.post("/conversations", response_model=dict, dependencies=[Depends(check_permission("use_ai_agent"))])
async def create_conversation(request: ConversationCreateRequest, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    conversation = ConversationService.create(db, current_user.id, request.title)
    return serialize_conversation(conversation, include_messages=True)


@router.get("/conversations/{conversation_id}", response_model=dict, dependencies=[Depends(check_permission("use_ai_agent"))])
async def get_conversation(conversation_id: str, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    conversation = ConversationService.get_for_user(db, conversation_id, current_user.id)
    return serialize_conversation(conversation, include_messages=True)


@router.patch("/conversations/{conversation_id}", response_model=dict, dependencies=[Depends(check_permission("use_ai_agent"))])
async def update_conversation(
    conversation_id: str,
    request: ConversationUpdateRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    conversation = ConversationService.set_archived(
        db, conversation_id, current_user.id, request.is_archived
    )
    return serialize_conversation(conversation)


@router.delete("/conversations/{conversation_id}", dependencies=[Depends(check_permission("use_ai_agent"))])
async def delete_conversation(
    conversation_id: str,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    ConversationService.delete_for_user(db, conversation_id, current_user.id)
    return {"status": "success", "message": "Conversation deleted"}


@router.post("/conversations/{conversation_id}/messages", response_model=dict, dependencies=[Depends(check_permission("use_ai_agent"))])
async def send_conversation_message(conversation_id: str, request: ConversationMessageRequest, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    conversation, user_message, assistant_message = await ConversationService.add_message(
        db, conversation_id, current_user.id, request.message, request.context, user=current_user
    )
    return {
        "conversation": serialize_conversation(conversation),
        "user_message": serialize_message(user_message),
        "assistant_message": serialize_message(assistant_message),
    }


@router.post("/conversations/{conversation_id}/messages/stream", dependencies=[Depends(check_permission("use_ai_agent"))])
async def stream_conversation_message(
    conversation_id: str,
    request: ConversationMessageRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Stream a persisted assistant response as server-sent events."""
    async def event_stream():
        async for chunk in ConversationService.stream_message(
            db, conversation_id, current_user.id, request.message, request.context, user=current_user
        ):
            yield f"data: {json.dumps({'type': 'chunk', 'content': chunk})}\n\n"
        yield "data: {\"type\": \"done\"}\n\n"

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@router.post("/query", response_model=dict, dependencies=[Depends(check_permission("use_ai_agent"))])
async def query_assistant(request: AssistantRequest, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    """Return an agent-backed investigation response grounded in authorized tool data."""
    from app.agents import SecurityAgent

    message = request.message.strip()
    agent = SecurityAgent(db, current_user)
    answer, provider, reasoning_details, tool_results = await agent.run(message, request.context, request.history)
    return {
        "answer": answer,
        "provider": provider,
        "mode": "security-agent",
        "reasoning_details": reasoning_details,
        "tool_calls": [
            {
                "tool": result["tool"],
                "status": result["status"],
                "error_message": result["error_message"],
                "summary": agent.result_summary(result) if result["status"] == "SUCCESS" else None,
            }
            for result in tool_results
        ],
    }


@router.get("/workflows", response_model=list[dict], dependencies=[Depends(check_permission("use_ai_agent"))])
async def list_workflows():
    """Return the catalog of application-data-driven AI investigation workflows."""
    from app.agents import WORKFLOW_CATALOG

    return WORKFLOW_CATALOG


@router.post("/workflows/alert-triage", response_model=dict, dependencies=[Depends(check_permission("use_ai_agent"))])
async def run_alert_triage(
    request: AlertTriageRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Triage one alert using its device, IP, related alerts, logs and linked investigation."""
    from app.agents import InvestigationWorkflow

    if request.conversation_id:
        ConversationService.get_for_user(db, request.conversation_id, current_user.id)
    workflow = InvestigationWorkflow(db, current_user)
    return await workflow.run_alert_triage(request.alert_id, request.conversation_id)


@router.post("/workflows/investigation-brief", response_model=dict, dependencies=[Depends(check_permission("use_ai_agent"))])
async def run_investigation_brief(
    request: InvestigationBriefRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Produce a case brief for one investigation from its alerts, evidence, notes and history."""
    from app.agents import InvestigationWorkflow

    if request.conversation_id:
        ConversationService.get_for_user(db, request.conversation_id, current_user.id)
    workflow = InvestigationWorkflow(db, current_user)
    return await workflow.run_investigation_brief(request.investigation_id, request.conversation_id)


@router.post("/tools/execute", response_model=dict, dependencies=[Depends(check_permission("use_ai_agent"))])
async def execute_investigation_tool(
    request: ToolExecutionRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Execute one bounded, permission-aware read tool for the assistant."""
    if request.conversation_id:
        ConversationService.get_for_user(db, request.conversation_id, current_user.id)

    started_at = perf_counter()
    try:
        result = SecurityInvestigationTools.execute(db, current_user, request.name, request.arguments)
        AuditService.record_tool_call(
            db,
            user_id=current_user.id,
            tool_name=request.name,
            arguments=request.arguments,
            result=result,
            status="SUCCESS",
            duration_ms=round((perf_counter() - started_at) * 1000),
            conversation_id=request.conversation_id,
        )
        return result
    except AppException as error:
        AuditService.record_tool_call(
            db,
            user_id=current_user.id,
            tool_name=request.name,
            arguments=request.arguments,
            result=None,
            status="FAILED",
            error_message=error.message,
            duration_ms=round((perf_counter() - started_at) * 1000),
            conversation_id=request.conversation_id,
        )
        raise
