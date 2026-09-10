# SentinelOps - Project Context

## Product

SentinelOps is a defensive SOC platform for monitoring alerts, investigating incidents, analyzing users, devices and IP addresses, searching logs, collecting evidence, tracking investigation timelines, calculating risk and using an AI Security Agent.

The AI is not a simple chatbot. It must use authorized backend tools and application services to inspect data and explain findings.

## Technology Stack

- Frontend: React, TypeScript, Vite, Redux Toolkit, Redux Saga, React Router, React Hook Form, Zod, Axios, Tailwind CSS, Recharts and Lucide React.
- Backend: Python 3.12, FastAPI, SQLAlchemy, Alembic, Pydantic, PostgreSQL, JWT and WebSockets.
- AI: provider abstraction with OpenRouter as the initial provider. AI keys remain on the backend.
- Infrastructure: Docker, Docker Compose and Git.

## Required Architecture

Frontend flow:

```text
Component -> dispatch(request) -> Saga -> API -> success/failure action
           -> Reducer -> Redux state -> Component
```

Backend flow:

```text
API -> Service -> Repository -> Database
```

AI flow:

```text
API -> Agent -> Tools -> Services -> Repository -> Database
```

Important rules:

- No API calls directly inside React components.
- Reducers only handle state transitions.
- Sagas handle asynchronous side effects.
- AI tools must be authorized, validate inputs, return structured results and use backend services.
- AI tools must never access the database directly.
- Use fictional defensive security data only.
- Do not implement offensive capabilities.

## Main Domain Areas

- Identity: users, roles, permissions and role assignments.
- Security: alerts, incidents, investigations, evidence and threats.
- Infrastructure: devices, IP addresses and locations.
- Activity: login events, log events, network events and timeline events.
- AI: conversations, messages and tool calls.
- System: notifications and audit logs.

Important relationships include users with devices, login events and alerts; devices with logs, network events and alerts; alerts with users, devices, IP addresses and investigations; and investigations with users, alerts, evidence, timeline events and notes.

## Authentication and Authorization

Authentication uses JWT. The defined roles are:

- `SOC_ADMIN`
- `SECURITY_ANALYST`
- `INVESTIGATOR`
- `VIEWER`

Authorization must exist on both frontend and backend. Frontend authorization is never sufficient for security.

## Development Phases

1. Phase 0: architecture and technical blueprint.
2. Phase 1: frontend foundation.
3. Phase 2: backend foundation.
4. Phase 3: authentication and authorization.
5. Phase 4: security domain: alerts, users, devices, IPs, logs, investigations and evidence.
6. Phase 5: dashboard.
7. Phase 6: investigation workflow.
8. Phase 7: advanced React features such as search, filters, pagination and URL state.
9. Phase 8: AI provider, agent, conversations and tools.
10. Phase 9: AI investigation workflows using application data.
11. Phase 10: WebSockets and live notifications.
12. Phase 11: testing, Docker hardening, logging, documentation and optimization.

## Current Repository Understanding

The repository has already progressed beyond the original Phase 0 starting point:

- Phase 0 is documented in `PHASE_0_BLUEPRINT.md`.
- The frontend foundation and backend foundation are present.
- JWT authentication, protected routes and initial permission handling are implemented.
- `backend/app/api/dependencies.py` contains the current JWT user dependency and role-permission checks.
- `SUPER_ADMIN_USERNAME`, `SUPER_ADMIN_EMAIL` and `SUPER_ADMIN_PASSWORD` optionally bootstrap one idempotent `SUPER_ADMIN` account at backend startup; the password is never stored in source code.
- The frontend store and root saga are prepared for additional feature slices and sagas.
- `PHASE_3_CHECKLIST.md` records Phase 3 as verified.

The repository is currently in Phase 4 implementation. Alerts, investigations, devices and logs have initial CRUD/API coverage. The latest Phase 4 work also separates read permissions from management permissions: viewers can read the permitted resources but cannot mutate them, and device access uses dedicated device permissions. Alert, investigation and device request payloads now use dedicated Pydantic schemas with validation. User, device, alert, investigation and log entities now expose ORM relationships with migration `008_link_security_entities`.

Evidence and investigation notes are now implemented as investigation-scoped resources with migration, validation, protected endpoints and frontend forms. The chatbot and AI Agent now share a backend AI service with an OpenRouter provider adapter; the API key remains server-side, Docker loads it from `backend/.env`, and OpenRouter retries/fallbacks are configurable. The AI service also uses a compact pre-prompt and input/output limits to reduce token usage, while the chat preserves recent messages. User/device/activity relationships and structured not-found service errors are now covered by migration `008_link_security_entities` and integration tests. IP intelligence is now covered by migration `009_add_ip_intelligence`, protected `/ip-addresses` endpoints, reputation validation and nested locations. Remaining Phase 4 work includes broader activity ingestion and frontend IP intelligence views.

The frontend now has a consistent visual layer for the Phase 4 screens: shared page framing, responsive navigation, status chips, field controls, interactive data rows and improved alert, investigation, device, log, IP intelligence and user role-management views. RBAC now includes a protected `SUPER_ADMIN` role: only super-admins can assign, modify or delete super-admin accounts.

## Reference Files

- `README.md`: project overview and high-level roadmap.
- `PHASE_0_BLUEPRINT.md`: architecture and data model blueprint.
- `PHASE_3_CHECKLIST.md`: authentication implementation checklist and next-phase requirements.
- `QUICK_REFERENCE.md`: startup commands, test credentials, URLs and key endpoints.
- `backend/README.md`: backend architecture and setup.
- `frontend/README.md`: frontend architecture and setup.
- `backend/app/api/dependencies.py`: current authentication and permission dependencies.

## Working Agreement

For every major phase:

1. Explain the objective.
2. List files to create or modify.
3. Implement only that phase.
4. Verify consistency with the architecture.
5. Provide commands to run and test.
6. Stop and wait for confirmation before starting the next major phase.
