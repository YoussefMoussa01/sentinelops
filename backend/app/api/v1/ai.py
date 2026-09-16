"""Investigation assistant API."""
from fastapi import APIRouter, Query
from typing import Any, Literal
from pydantic import BaseModel, Field
from fastapi import Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.api.dependencies import check_permission, get_current_user
from app.services.ai_service import AIService
from app.services import ConversationService
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


@router.get("/conversations", response_model=list[dict[str, Any]], dependencies=[Depends(check_permission("use_ai_agent"))])
async def list_conversations(
    include_archived: bool = Query(default=False),
    search: str | None = Query(default=None, max_length=100),
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """List only conversations owned by the authenticated user."""
    return [serialize_conversation(item) for item in ConversationService.list_for_user(db, current_user.id, include_archived, search)]


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
        db, conversation_id, current_user.id, request.message, request.context
    )
    return {
        "conversation": serialize_conversation(conversation),
        "user_message": serialize_message(user_message),
        "assistant_message": serialize_message(assistant_message),
    }


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


@router.post("/tools/execute", response_model=dict, dependencies=[Depends(check_permission("use_ai_agent"))])
async def execute_investigation_tool(
    request: ToolExecutionRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Execute one bounded, permission-aware read tool for the assistant."""
    return SecurityInvestigationTools.execute(db, current_user, request.name, request.arguments)
