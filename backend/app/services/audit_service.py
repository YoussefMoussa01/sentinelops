"""Persistence service for AI tool calls and security audit events."""
from datetime import datetime, timezone
from typing import Any

from sqlalchemy.orm import Session

from app.models import AIToolCall, AuditEvent


class AuditService:
    @staticmethod
    def list_tool_calls(db: Session, user_id: str, limit: int = 50) -> list[AIToolCall]:
        return (
            db.query(AIToolCall)
            .filter(AIToolCall.user_id == user_id)
            .order_by(AIToolCall.created_at.desc())
            .limit(limit)
            .all()
        )

    @staticmethod
    def record_tool_call(
        db: Session,
        *,
        user_id: str,
        tool_name: str,
        arguments: dict[str, Any],
        result: dict[str, Any] | None,
        status: str,
        error_message: str | None = None,
        duration_ms: int | None = None,
        conversation_id: str | None = None,
    ) -> AIToolCall:
        tool_call = AIToolCall(
            user_id=user_id,
            conversation_id=conversation_id,
            tool_name=tool_name,
            arguments=arguments,
            result=result,
            status=status,
            error_message=error_message,
            duration_ms=duration_ms,
        )
        db.add(tool_call)
        db.add(AuditEvent(
            actor_user_id=user_id,
            action="ai_tool.execute",
            resource_type="AI_TOOL",
            resource_id=tool_name,
            event_metadata={"status": status, "conversation_id": conversation_id},
        ))
        db.commit()
        db.refresh(tool_call)
        return tool_call
