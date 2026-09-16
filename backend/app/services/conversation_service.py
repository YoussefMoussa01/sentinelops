"""Persistence and orchestration for assistant conversations."""
from datetime import datetime, timezone
from typing import Any

from sqlalchemy import or_
from sqlalchemy.orm import Session, joinedload

from app.core.exceptions import NotFoundError
from app.models import AIConversation, AIMessage
from app.services.ai_service import AIService


class ConversationService:
    DEFAULT_TITLES = {"New SentinelOps conversation", "AI investigation workspace", "SentinelOps assistant"}

    @staticmethod
    def generate_title(content: str) -> str:
        """Create a compact, deterministic title without another provider call."""
        title = " ".join(content.split()).strip()
        if not title:
            return "New SentinelOps conversation"
        first_sentence = title.split(".", 1)[0].strip()
        return first_sentence[:80].rstrip() or "New SentinelOps conversation"

    @staticmethod
    def create(db: Session, user_id: str, title: str | None = None) -> AIConversation:
        conversation = AIConversation(
            user_id=user_id,
            title=(title or "New SentinelOps conversation").strip()[:200],
        )
        db.add(conversation)
        db.commit()
        db.refresh(conversation)
        return conversation

    @staticmethod
    def list_for_user(
        db: Session,
        user_id: str,
        include_archived: bool = False,
        search: str | None = None,
    ) -> list[AIConversation]:
        query = db.query(AIConversation).filter(AIConversation.user_id == user_id)
        if not include_archived:
            query = query.filter(AIConversation.is_archived.is_(False))
        if search and search.strip():
            pattern = f"%{search.strip()}%"
            query = query.filter(
                or_(
                    AIConversation.title.ilike(pattern),
                    AIConversation.messages.any(AIMessage.content.ilike(pattern)),
                )
            )
        return (
            query
            .order_by(AIConversation.updated_at.desc())
            .all()
        )

    @staticmethod
    def get_for_user(db: Session, conversation_id: str, user_id: str) -> AIConversation:
        conversation = (
            db.query(AIConversation)
            .options(joinedload(AIConversation.messages))
            .filter(AIConversation.id == conversation_id, AIConversation.user_id == user_id)
            .first()
        )
        if not conversation:
            raise NotFoundError("Conversation")
        return conversation

    @staticmethod
    def set_archived(
        db: Session, conversation_id: str, user_id: str, is_archived: bool
    ) -> AIConversation:
        conversation = ConversationService.get_for_user(db, conversation_id, user_id)
        conversation.is_archived = is_archived
        db.commit()
        db.refresh(conversation)
        return conversation

    @staticmethod
    def delete_for_user(db: Session, conversation_id: str, user_id: str) -> None:
        conversation = ConversationService.get_for_user(db, conversation_id, user_id)
        db.delete(conversation)
        db.commit()

    @staticmethod
    async def add_message(
        db: Session,
        conversation_id: str,
        user_id: str,
        content: str,
        context: str | None = None,
    ) -> tuple[AIConversation, AIMessage, AIMessage]:
        conversation = ConversationService.get_for_user(db, conversation_id, user_id)
        history: list[dict[str, Any]] = [
            {
                "role": item.role,
                "content": item.content,
                **({"reasoning_details": item.reasoning_details} if item.reasoning_details is not None else {}),
            }
            for item in conversation.messages[-8:]
        ]

        user_message = AIMessage(conversation_id=conversation.id, role="user", content=content.strip())
        db.add(user_message)
        answer, provider, reasoning_details = await AIService.answer(content, context, history)
        assistant_message = AIMessage(
            conversation_id=conversation.id,
            role="assistant",
            content=answer,
            provider=provider,
            reasoning_details=reasoning_details,
        )
        db.add(assistant_message)
        if conversation.title in ConversationService.DEFAULT_TITLES:
            conversation.title = ConversationService.generate_title(content)
        conversation.updated_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(conversation)
        db.refresh(user_message)
        db.refresh(assistant_message)
        return conversation, user_message, assistant_message
