# Phase 8 - AI Conversations Progress

## Delivered

- Persistent `AIConversation` and `AIMessage` models.
- Alembic migration `012_add_ai_conversations`.
- User-scoped conversation listing and retrieval.
- Ownership isolation: users cannot read another user's conversations.
- Persistent user and assistant messages.
- OpenRouter/fallback responses reused through `AIService`.
- AI page connected to conversation/message endpoints.
- Chat widget creates and persists a platform-wide assistant conversation.
- Backend integration coverage for persistence and RBAC isolation.
- Conversation archive/restore and permanent deletion with ownership protection.
- Active conversation listing excludes archived records by default.
- AI workspace now exposes conversation history and lifecycle actions.
- Server-side deterministic titles generated from the first user message.
- Conversation search covers titles and message content.
- Added permission-aware read-only AI tools for alerts, devices, logs and IP intelligence.
- Tool execution validates tool names, role permissions and result limits.

## Next Tasks

- Store tool calls and audit events.
- Add streaming responses for the chat widget.
- Add frontend conversation history and loading states.
