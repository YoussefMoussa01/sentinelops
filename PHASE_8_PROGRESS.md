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
- Added persistent AI tool-call records and security audit events with user ownership.
- Added a user-scoped endpoint for reviewing AI tool execution history.
- Added SSE streaming for persisted conversation responses.
- Chat widget now renders streamed assistant chunks progressively.
- OpenRouter native SSE deltas are now forwarded when live provider streaming is available.

## Next Tasks

- Add frontend conversation history and loading states.
