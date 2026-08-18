# SentinelOps — Phase 0: Technical Blueprint

**Project**: AI-powered cybersecurity investigation platform  
**Status**: Architecture Design  
**Date**: 2026-08-18

---

## 1. Repository Structure

```
sentinelops/
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── store/
│   │   │   │   ├── store.ts
│   │   │   │   └── hooks.ts
│   │   │   └── router/
│   │   │       └── routes.tsx
│   │   ├── pages/
│   │   │   ├── LoginPage.tsx
│   │   │   ├── DashboardPage.tsx
│   │   │   ├── AlertsPage.tsx
│   │   │   ├── AlertDetailPage.tsx
│   │   │   ├── InvestigationsPage.tsx
│   │   │   ├── InvestigationDetailPage.tsx
│   │   │   ├── UsersPage.tsx
│   │   │   ├── UserDetailPage.tsx
│   │   │   ├── DevicesPage.tsx
│   │   │   ├── DeviceDetailPage.tsx
│   │   │   ├── LogsPage.tsx
│   │   │   ├── AiPage.tsx
│   │   │   └── AdminPage.tsx
│   │   ├── components/
│   │   │   ├── Layout.tsx
│   │   │   ├── Header.tsx
│   │   │   ├── Sidebar.tsx
│   │   │   ├── ProtectedRoute.tsx
│   │   │   └── [shared components]
│   │   ├── features/
│   │   │   ├── auth/
│   │   │   │   ├── state/
│   │   │   │   │   └── authSlice.ts
│   │   │   │   ├── sagas/
│   │   │   │   │   └── authSagas.ts
│   │   │   │   ├── types/
│   │   │   │   │   └── auth.types.ts
│   │   │   │   ├── hooks/
│   │   │   │   │   └── useAuth.ts
│   │   │   │   └── index.ts
│   │   │   ├── alerts/
│   │   │   │   ├── state/
│   │   │   │   ├── sagas/
│   │   │   │   ├── types/
│   │   │   │   └── index.ts
│   │   │   ├── investigations/
│   │   │   │   ├── state/
│   │   │   │   ├── sagas/
│   │   │   │   ├── types/
│   │   │   │   └── index.ts
│   │   │   ├── users/
│   │   │   ├── devices/
│   │   │   ├── logs/
│   │   │   ├── ai/
│   │   │   │   ├── state/
│   │   │   │   │   └── aiSlice.ts
│   │   │   │   ├── sagas/
│   │   │   │   │   └── aiSagas.ts
│   │   │   │   ├── types/
│   │   │   │   └── index.ts
│   │   │   └── dashboard/
│   │   ├── hooks/
│   │   │   ├── usePagination.ts
│   │   │   ├── useUrlState.ts
│   │   │   └── useAuth.ts
│   │   ├── services/
│   │   │   ├── api/
│   │   │   │   ├── client.ts
│   │   │   │   ├── auth.api.ts
│   │   │   │   ├── alerts.api.ts
│   │   │   │   ├── investigations.api.ts
│   │   │   │   ├── users.api.ts
│   │   │   │   ├── devices.api.ts
│   │   │   │   ├── logs.api.ts
│   │   │   │   └── ai.api.ts
│   │   │   └── localStorage.ts
│   │   ├── types/
│   │   │   ├── api.types.ts
│   │   │   └── errors.types.ts
│   │   ├── data-types/
│   │   │   ├── Alert.ts
│   │   │   ├── User.ts
│   │   │   ├── Device.ts
│   │   │   ├── Investigation.ts
│   │   │   ├── AIMessage.ts
│   │   │   └── [other domain types]
│   │   ├── utils/
│   │   │   ├── storage.ts
│   │   │   ├── date.ts
│   │   │   └── validation.ts
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── index.html
│   ├── package.json
│   ├── vite.config.ts
│   ├── tsconfig.json
│   ├── tailwind.config.js
│   ├── .env.example
│   └── .gitignore
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── v1/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── auth.py
│   │   │   │   ├── alerts.py
│   │   │   │   ├── investigations.py
│   │   │   │   ├── users.py
│   │   │   │   ├── devices.py
│   │   │   │   ├── logs.py
│   │   │   │   ├── ai.py
│   │   │   │   └── admin.py
│   │   │   └── dependencies.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── identity.py (User, Role, Permission)
│   │   │   ├── security.py (Alert, Incident, Investigation)
│   │   │   ├── infrastructure.py (Device, IPAddress, Location)
│   │   │   ├── activity.py (LoginEvent, LogEvent, NetworkEvent)
│   │   │   ├── evidence.py (Evidence, InvestigationEvidence)
│   │   │   └── ai.py (AIConversation, AIMessage, AIToolCall)
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── alert.py
│   │   │   ├── investigation.py
│   │   │   ├── user.py
│   │   │   ├── device.py
│   │   │   ├── logs.py
│   │   │   ├── ai.py
│   │   │   └── common.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── alert_service.py
│   │   │   ├── investigation_service.py
│   │   │   ├── user_service.py
│   │   │   ├── device_service.py
│   │   │   ├── log_service.py
│   │   │   ├── ai_service.py
│   │   │   └── risk_service.py
│   │   ├── repositories/
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   ├── alert_repository.py
│   │   │   ├── investigation_repository.py
│   │   │   ├── user_repository.py
│   │   │   ├── device_repository.py
│   │   │   └── log_repository.py
│   │   ├── agents/
│   │   │   ├── __init__.py
│   │   │   ├── security_agent.py
│   │   │   └── base.py
│   │   ├── tools/
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   ├── user_tools.py
│   │   │   ├── device_tools.py
│   │   │   ├── alert_tools.py
│   │   │   ├── log_tools.py
│   │   │   ├── investigation_tools.py
│   │   │   ├── ip_tools.py
│   │   │   └── risk_tools.py
│   │   ├── providers/
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   ├── openrouter.py
│   │   │   └── factory.py
│   │   ├── database/
│   │   │   ├── __init__.py
│   │   │   ├── session.py
│   │   │   ├── config.py
│   │   │   └── migrations/
│   │   │       ├── env.py
│   │   │       ├── script.py.mako
│   │   │       └── versions/
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── config.py
│   │   │   ├── security.py
│   │   │   ├── exceptions.py
│   │   │   ├── logging.py
│   │   │   └── constants.py
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── pagination.py
│   │       └── validators.py
│   ├── requirements.txt
│   ├── .env.example
│   ├── alembic.ini
│   └── .gitignore
├── docker-compose.yml
├── Dockerfile.frontend
├── Dockerfile.backend
├── .gitignore
└── README.md
```

---

## 2. Database Schema

### 2.1 Entity Relationships

```
┌─────────────────────────────────────────────────────────────┐
│                      IDENTITY DOMAIN                         │
├─────────────────────────────────────────────────────────────┤
User (1:N Device, 1:N LoginEvent, 1:N Alert, N:N Investigation)
├── id (PK)
├── username (unique)
├── email (unique)
├── password_hash
├── is_active
├── created_at
├── updated_at

Role (N:N User via UserRole)
├── id (PK)
├── name (SOC_ADMIN, SECURITY_ANALYST, INVESTIGATOR, VIEWER)
├── description

Permission
├── id (PK)
├── name
├── description

UserRole
├── user_id (FK)
├── role_id (FK)

RolePermission
├── role_id (FK)
├── permission_id (FK)

┌─────────────────────────────────────────────────────────────┐
│                   INFRASTRUCTURE DOMAIN                      │
├─────────────────────────────────────────────────────────────┤
Device (N:1 User, 1:N LoginEvent, 1:N LogEvent, 1:N NetworkEvent)
├── id (PK)
├── user_id (FK)
├── name
├── type (laptop, server, mobile, etc.)
├── os
├── ip_address (current)
├── is_active
├── created_at
├── updated_at

IPAddress (N:M Device)
├── id (PK)
├── address (unique)
├── is_private
├── country
├── city
├── latitude
├── longitude
├── reputation_score (0-100, fictional)
├── created_at

Location
├── id (PK)
├── ip_address_id (FK)
├── country
├── city
├── latitude
├── longitude
├── timezone

┌─────────────────────────────────────────────────────────────┐
│                    SECURITY DOMAIN                           │
├─────────────────────────────────────────────────────────────┤
Alert (N:1 User, N:1 Device, N:1 IPAddress, N:1 Incident, N:N Investigation)
├── id (PK)
├── user_id (FK, nullable)
├── device_id (FK, nullable)
├── ip_address_id (FK, nullable)
├── incident_id (FK, nullable)
├── title
├── description
├── severity (LOW, MEDIUM, HIGH, CRITICAL)
├── status (NEW, ACKNOWLEDGED, INVESTIGATING, RESOLVED, FALSE_POSITIVE)
├── source
├── detection_time
├── created_at
├── updated_at

Incident
├── id (PK)
├── title
├── description
├── severity
├── status
├── created_at
├── updated_at

Investigation (N:N User, N:N Alert, N:N Evidence, 1:N TimelineEvent)
├── id (PK)
├── title
├── description
├── status (OPEN, CLOSED, ARCHIVED)
├── severity
├── risk_score (0-100, fictional)
├── created_by (FK -> User)
├── created_at
├── updated_at

InvestigationMember
├── investigation_id (FK)
├── user_id (FK)
├── role (OWNER, ANALYST, VIEWER)
├── joined_at

InvestigationAlert
├── investigation_id (FK)
├── alert_id (FK)

InvestigationEvidence
├── investigation_id (FK)
├── evidence_id (FK)

TimelineEvent
├── id (PK)
├── investigation_id (FK)
├── event_type (alert, login, log, network, note, etc.)
├── entity_id (FK to related entity)
├── description
├── occurred_at
├── created_at

InvestigationNote
├── id (PK)
├── investigation_id (FK)
├── created_by (FK -> User)
├── content
├── is_pinned
├── created_at
├── updated_at

Evidence
├── id (PK)
├── investigation_id (FK)
├── title
├── description
├── source
├── data (JSON, can store structured or raw data)
├── created_by (FK -> User)
├── created_at

┌─────────────────────────────────────────────────────────────┐
│                     ACTIVITY DOMAIN                          │
├─────────────────────────────────────────────────────────────┤
LoginEvent (N:1 User, N:1 Device, N:1 IPAddress)
├── id (PK)
├── user_id (FK)
├── device_id (FK, nullable)
├── ip_address_id (FK, nullable)
├── timestamp
├── success
├── method (password, mfa, sso)
├── risk_score (0-100, fictional)

LogEvent (N:1 Device)
├── id (PK)
├── device_id (FK)
├── log_type (auth, firewall, application, system)
├── level (INFO, WARNING, ERROR, CRITICAL)
├── message
├── source
├── timestamp
├── raw_data (JSON)

NetworkEvent (N:1 Device)
├── id (PK)
├── device_id (FK)
├── source_ip (FK -> IPAddress, nullable)
├── destination_ip (FK -> IPAddress, nullable)
├── port
├── protocol
├── bytes_transferred
├── timestamp
├── risk_score (0-100, fictional)

┌─────────────────────────────────────────────────────────────┐
│                       AI DOMAIN                              │
├─────────────────────────────────────────────────────────────┤
AIConversation
├── id (PK)
├── investigation_id (FK)
├── created_by (FK -> User)
├── title
├── is_active
├── created_at
├── updated_at

AIMessage
├── id (PK)
├── conversation_id (FK)
├── role (USER, ASSISTANT, TOOL, SYSTEM)
├── content
├── metadata (JSON, may include tool calls)
├── created_at

AIToolCall
├── id (PK)
├── message_id (FK)
├── tool_name
├── input (JSON)
├── output (JSON)
├── status (PENDING, SUCCESS, FAILED)
├── execution_time_ms
├── created_at

┌─────────────────────────────────────────────────────────────┐
│                     SYSTEM DOMAIN                            │
├─────────────────────────────────────────────────────────────┤
Notification
├── id (PK)
├── user_id (FK)
├── type (alert, investigation, system)
├── title
├── message
├── is_read
├── data (JSON)
├── created_at

AuditLog
├── id (PK)
├── user_id (FK)
├── action
├── resource_type
├── resource_id
├── details (JSON)
├── ip_address
├── created_at
```

### 2.2 Critical Relationships

| Relationship | Type | Notes |
|---|---|---|
| User → Device | 1:N | One user can have multiple devices |
| User → LoginEvent | 1:N | Track all login events by user |
| User → Alert | 1:N | Alerts may target a user |
| User → Investigation | N:N | Multiple users collaborate on investigations |
| Device → LogEvent | 1:N | Each device generates logs |
| Device → NetworkEvent | 1:N | Network activity per device |
| Alert → Investigation | N:N | Alerts linked to investigations via join table |
| Alert → User | N:1 | Alert may target a user |
| Alert → Device | N:1 | Alert may target a device |
| Alert → IPAddress | N:1 | Alert may involve an IP |
| Investigation → Evidence | N:N | Multiple evidence items per investigation |
| Investigation → TimelineEvent | 1:N | Timeline is immutable history |
| IPAddress → Location | 1:1 | IP enrichment with geolocation |

---

## 3. API Architecture

### 3.1 REST Endpoints

#### Authentication
```
POST   /api/v1/auth/login
POST   /api/v1/auth/logout
POST   /api/v1/auth/refresh
GET    /api/v1/auth/me
```

#### Alerts
```
GET    /api/v1/alerts
GET    /api/v1/alerts/:id
PATCH  /api/v1/alerts/:id
PATCH  /api/v1/alerts/:id/status
```

#### Investigations
```
GET    /api/v1/investigations
POST   /api/v1/investigations
GET    /api/v1/investigations/:id
PATCH  /api/v1/investigations/:id
DELETE /api/v1/investigations/:id
GET    /api/v1/investigations/:id/timeline
POST   /api/v1/investigations/:id/notes
POST   /api/v1/investigations/:id/evidence
POST   /api/v1/investigations/:id/members
DELETE /api/v1/investigations/:id/members/:userId
```

#### Users
```
GET    /api/v1/users
GET    /api/v1/users/:id
GET    /api/v1/users/:id/login-events
GET    /api/v1/users/:id/alerts
```

#### Devices
```
GET    /api/v1/devices
GET    /api/v1/devices/:id
GET    /api/v1/devices/:id/events
GET    /api/v1/devices/:id/alerts
```

#### Logs
```
GET    /api/v1/logs
GET    /api/v1/logs/search
```

#### AI
```
POST   /api/v1/ai/conversations
GET    /api/v1/ai/conversations/:id
POST   /api/v1/ai/conversations/:id/messages
GET    /api/v1/ai/conversations/:id/messages
```

#### Admin
```
GET    /api/v1/admin/users
POST   /api/v1/admin/users
PATCH  /api/v1/admin/users/:id
DELETE /api/v1/admin/users/:id
POST   /api/v1/admin/roles
GET    /api/v1/admin/audit-logs
```

### 3.2 Response Format

**Success Response:**
```json
{
  "status": "success",
  "data": { /* payload */ },
  "meta": {
    "timestamp": "2026-08-18T10:30:00Z"
  }
}
```

**Paginated Response:**
```json
{
  "status": "success",
  "data": [ /* items */ ],
  "meta": {
    "timestamp": "2026-08-18T10:30:00Z",
    "pagination": {
      "page": 1,
      "page_size": 20,
      "total": 150,
      "total_pages": 8
    }
  }
}
```

**Error Response:**
```json
{
  "status": "error",
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "Alert not found",
    "details": null
  },
  "meta": {
    "timestamp": "2026-08-18T10:30:00Z"
  }
}
```

### 3.3 Error Codes

| Code | HTTP | Description |
|---|---|---|
| INVALID_CREDENTIALS | 401 | Login failed |
| UNAUTHORIZED | 403 | User lacks permission |
| RESOURCE_NOT_FOUND | 404 | Resource doesn't exist |
| VALIDATION_ERROR | 400 | Input validation failed |
| CONFLICT | 409 | Resource conflict (duplicate, etc.) |
| SERVER_ERROR | 500 | Unexpected server error |
| AI_ERROR | 500 | AI provider error |

---

## 4. Redux & Saga Architecture

### 4.1 Redux Store Structure

```typescript
// store.ts
{
  auth: {
    isLoading: boolean
    user: User | null
    token: string | null
    error: string | null
  }
  
  alerts: {
    isLoading: boolean
    items: Alert[]
    filters: AlertFilters
    pagination: Pagination
    error: string | null
  }
  
  investigations: {
    isLoading: boolean
    items: Investigation[]
    current: Investigation | null
    currentTimeline: TimelineEvent[]
    filters: InvestigationFilters
    pagination: Pagination
    error: string | null
  }
  
  users: {
    isLoading: boolean
    items: User[]
    current: User | null
    pagination: Pagination
    error: string | null
  }
  
  devices: {
    isLoading: boolean
    items: Device[]
    current: Device | null
    pagination: Pagination
    error: string | null
  }
  
  logs: {
    isLoading: boolean
    items: LogEvent[]
    filters: LogFilters
    pagination: Pagination
    error: string | null
  }
  
  ai: {
    isLoading: boolean
    conversations: AIConversation[]
    currentConversation: AIConversation | null
    messages: AIMessage[]
    toolExecutionState: ToolExecutionState | null
    error: string | null
  }
}
```

### 4.2 Saga Flow Example (Alerts)

```
Component
  ↓
dispatch(fetchAlerts({ page: 1, severity: 'HIGH' }))
  ↓
alertsSaga.ts (watchFetchAlerts)
  ↓
call(alertsAPI.getAlerts())
  ↓
Backend REST
  ↓
put(fetchAlertsSuccess(data))
  ↓
alertsSlice reducer
  ↓
Redux state updated
  ↓
Component selector reads state
  ↓
Component re-renders
```

### 4.3 Feature Slice Structure

Each feature follows this pattern:

**state/xxxSlice.ts** — Redux Toolkit slice
- Actions (auto-generated and custom)
- Reducers
- Selectors

**sagas/xxxSagas.ts** — Side effects
- Watchers (fork, takeLatest, takeEvery)
- Workers (call API, dispatch actions)
- Error handling

**types/xxx.types.ts** — TypeScript interfaces
- Domain models
- API request/response types
- UI state types

**hooks/useXxx.ts** — Custom hooks
- useSelector shortcuts
- useDispatch shortcuts
- Local component state

**index.ts** — Public API
- Export slice, actions, selectors
- Export saga factory

### 4.4 Root Saga

```typescript
// sagas/rootSaga.ts
function* rootSaga() {
  yield fork(authSaga)
  yield fork(alertsSaga)
  yield fork(investigationsSaga)
  yield fork(usersSaga)
  yield fork(devicesSaga)
  yield fork(logsSaga)
  yield fork(aiSaga)
}
```

---

## 5. AI Architecture

### 5.1 Provider Abstraction

```
AIProvider (interface)
├── OpenRouterProvider (implementation)
├── Future: AnthropicProvider
└── Future: AzureOpenAIProvider

SecurityAgent
├── uses AIProvider
├── executes Tools
└── manages Conversation
```

### 5.2 AI Service Flow

```
API: POST /api/v1/ai/conversations/:id/messages
  ↓
AIService.processUserMessage(conversationId, userMessage)
  ↓
SecurityAgent.run(userMessage, context)
  ↓
1. Add user message to conversation
2. Get conversation history
3. Call AIProvider.chat(messages, tools)
4. Parse response (text + tool calls)
5. Execute tools (get structured results)
6. Add assistant message to conversation
7. Add tool messages to conversation
8. Return to client
  ↓
Response: { message, toolExecutions }
```

### 5.3 Tool Architecture

```
ToolBase (abstract)
├── name: str
├── description: str
├── input_schema: dict (JSON Schema)
├── execute(input) → dict
├── authorize(user, input) → bool
├── validate(input) → bool

Concrete Tools:
├── SearchUsersToolTool
├── GetUserDetailsTool
├── SearchDevicesTool
├── GetDeviceDetailsTool
├── SearchAlertsTool
├── GetAlertDetailsTool
├── SearchLogsTool
├── SearchLoginEventsTool
├── GetIPDetailsTool
├── GetIPActivityTool
├── GetInvestigationTool
├── GetInvestigationTimelineTool
├── CalculateRiskScoreTool
├── CreateInvestigationTool
├── UpdateInvestigationTool
├── AddInvestigationNoteTool
├── AddEvidenceTool
└── SearchNetworkEventsTool
```

### 5.4 Tool Design Rules

1. **Authorization**: Each tool checks user permissions
2. **Validation**: Input validated against schema before execution
3. **Services**: Tools call services (not repositories directly)
4. **Structure**: Return structured data (not raw DB objects)
5. **Error Handling**: Meaningful error messages
6. **Logging**: All tool calls logged for audit

Example Tool:

```python
class SearchUsersTool(ToolBase):
    name = "search_users"
    description = "Search for users by name, email, or username"
    input_schema = {
        "type": "object",
        "properties": {
            "query": {"type": "string"},
            "limit": {"type": "integer", "default": 10}
        }
    }
    
    def authorize(self, user: User, input_data: dict) -> bool:
        return user.has_permission("search_users")
    
    def validate(self, input_data: dict) -> bool:
        return len(input_data["query"]) > 0
    
    def execute(self, input_data: dict) -> dict:
        results = self.user_service.search(
            query=input_data["query"],
            limit=input_data.get("limit", 10)
        )
        return {
            "found": len(results),
            "users": [
                {
                    "id": u.id,
                    "username": u.username,
                    "email": u.email,
                    "is_active": u.is_active
                }
                for u in results
            ]
        }
```

### 5.5 AI Conversation Flow

```
AIConversation
├── id
├── investigation_id (nullable)
├── created_by
├── messages: [
│   ├── AIMessage (role: USER)
│   │   └── content: "Investigate Sarah's login yesterday"
│   ├── AIMessage (role: ASSISTANT)
│   │   └── content: "I'll help. Let me search for Sarah first."
│   ├── AIMessage (role: TOOL)
│   │   └── content: { tool_name, output }
│   ├── AIMessage (role: TOOL)
│   │   └── content: { tool_name, output }
│   ├── AIMessage (role: ASSISTANT)
│   │   └── content: "I found 3 suspicious logins..."
│   └── ...
│   ]
```

### 5.6 Configuration

```python
# .env
AI_PROVIDER=openrouter
OPENROUTER_API_KEY=<secret>
AI_MODEL=openai/gpt-4
AI_TEMPERATURE=0.7
AI_MAX_TOKENS=2000
```

---

## 6. Authentication & Authorization

### 6.1 JWT Flow

```
1. User login (username + password)
2. Backend validates credentials
3. Backend generates JWT (access + optional refresh)
4. Frontend stores token in localStorage
5. Frontend sends Authorization: Bearer <token> on requests
6. Backend verifies token on each request
7. Token expiry: frontend detects 401, requests refresh
8. Backend validates refresh token, issues new access token
9. Frontend retries original request
10. Logout clears token from localStorage
```

### 6.2 Token Structure

```json
{
  "sub": "user_id",
  "username": "jane.doe",
  "roles": ["SECURITY_ANALYST"],
  "permissions": ["view_alerts", "search_users"],
  "iat": 1692374400,
  "exp": 1692378000
}
```

### 6.3 Roles & Permissions

**Roles:**
- `SOC_ADMIN` — Full platform access, user management
- `SECURITY_ANALYST` — View/manage alerts, create investigations
- `INVESTIGATOR` — Full investigation workflow, edit notes
- `VIEWER` — Read-only access to alerts and investigations

**Permissions** (examples):
- `view_alerts`
- `manage_alerts`
- `create_investigation`
- `edit_investigation`
- `view_users`
- `manage_users`
- `use_ai_agent`
- `edit_risk_score`

### 6.4 Frontend Authorization

**Protected Routes:**
```tsx
<ProtectedRoute 
  requiredRole="INVESTIGATOR" 
  element={<InvestigationDetailPage />} 
/>
```

**Permission Guards:**
```tsx
{user?.permissions.includes('manage_alerts') && (
  <button onClick={handleResolve}>Resolve Alert</button>
)}
```

**Session Restoration:**
```tsx
// On app load, check if token exists
// Call /api/v1/auth/me to validate and restore user
// On 401, redirect to login
```

---

## 7. Environment Variables

### Frontend (.env)

```
VITE_API_BASE_URL=http://localhost:8000/api/v1
VITE_AUTH_REDIRECT_LOGIN=/login
VITE_AUTH_REDIRECT_DEFAULT=/dashboard
VITE_TOKEN_STORAGE_KEY=sentinelops_token
VITE_USER_STORAGE_KEY=sentinelops_user
```

### Backend (.env)

```
# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/sentinelops_db

# JWT
JWT_SECRET_KEY=<random-secret-key>
JWT_ALGORITHM=HS256
JWT_EXPIRATION_SECONDS=3600
JWT_REFRESH_EXPIRATION_SECONDS=604800

# API
API_V1_PREFIX=/api/v1
API_TITLE=SentinelOps API
API_VERSION=0.1.0

# CORS
CORS_ORIGINS=http://localhost:5173,http://localhost:3000

# AI
AI_PROVIDER=openrouter
OPENROUTER_API_KEY=<secret>
AI_MODEL=openai/gpt-4
AI_TEMPERATURE=0.7
AI_MAX_TOKENS=2000

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/sentinelops.log

# Security
ALLOWED_HOSTS=localhost,127.0.0.1
DEBUG=False
```

---

## 8. Docker Architecture

### 8.1 Services

```yaml
services:
  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: sentinelops
      POSTGRES_PASSWORD: sentinelops_pass
      POSTGRES_DB: sentinelops_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  backend:
    build:
      context: .
      dockerfile: Dockerfile.backend
    environment:
      DATABASE_URL: postgresql://sentinelops:sentinelops_pass@postgres:5432/sentinelops_db
    ports:
      - "8000:8000"
    depends_on:
      - postgres
    volumes:
      - ./backend:/app
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

  frontend:
    build:
      context: ./frontend
      dockerfile: ../Dockerfile.frontend
    ports:
      - "5173:5173"
    environment:
      VITE_API_BASE_URL: http://backend:8000/api/v1
    depends_on:
      - backend
    volumes:
      - ./frontend:/app

volumes:
  postgres_data:
```

### 8.2 Dockerfiles

**Dockerfile.backend:**
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/app ./app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Dockerfile.frontend:**
```dockerfile
FROM node:20-alpine as build
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

---

## 9. Development Order

### Phase Sequence:

1. **Phase 0** — Architecture (current)
2. **Phase 1** — Frontend Foundation
3. **Phase 2** — Backend Foundation
4. **Phase 3** — Authentication
5. **Phase 4** — Security Domain (Alerts, Users, Devices, Logs)
6. **Phase 5** — Dashboard
7. **Phase 6** — Investigation Workflow
8. **Phase 7** — Advanced React (Search, Filters, Pagination)
9. **Phase 8** — AI Provider & Agent
10. **Phase 9** — AI Tools & Integration
11. **Phase 10** — Real-Time (WebSockets)
12. **Phase 11** — Testing & Production

---

## 10. Key Architectural Decisions

### 10.1 State Management

**Decision**: Use Redux Toolkit + Redux Saga
- **Rationale**: Predictable state, clear async patterns, excellent TypeScript support, proven at scale
- **Alternative Rejected**: Context API (too verbose for complex state), Zustand (less structured for large teams)

### 10.2 Database

**Decision**: PostgreSQL with SQLAlchemy ORM
- **Rationale**: Strong relational integrity, JSON support, excellent Python ecosystem
- **Alternative Rejected**: MongoDB (not ideal for relational security data)

### 10.3 API Strategy

**Decision**: RESTful JSON API with pagination
- **Rationale**: Simple, well-understood, good fit for CRUD operations
- **Future**: WebSockets for real-time alerts (Phase 10)

### 10.4 AI Architecture

**Decision**: Provider abstraction with OpenRouter as default
- **Rationale**: Allows model switching, reduces vendor lock-in, abstraction enables testing
- **Tool Authorization**: Backend validates all tool calls against user permissions

### 10.5 Frontend Structure

**Decision**: Features folder with Redux slice per domain
- **Rationale**: Scalable, easy to find domain logic, reduces cross-domain coupling

---

## 11. Missing Decisions or Contradictions

### 11.1 Potential Questions

1. **Caching Strategy**: Should we cache alert lists? Device data? How long?
   - *Recommendation*: Implement simple Redux cache with timestamp, invalidate on mutations

2. **Audit Trail Depth**: How much detail in AuditLog? Every read or only writes?
   - *Recommendation*: Log writes only in Phase 1, consider read logging in Phase 11

3. **Risk Score Algorithm**: How is risk calculated? Who defines it?
   - *Recommendation*: Implement placeholder algorithm in Phase 4, document that it's fictional

4. **Real-time Scalability**: How many concurrent WebSocket connections to support?
   - *Recommendation*: Plan for Phase 10; defer architectural decision until then

5. **Search Performance**: Full-text search or indexed queries?
   - *Recommendation*: Start with indexed queries (Phase 7), consider FTS in Phase 11

6. **File Storage for Evidence**: Where do uploaded evidence files live?
   - *Recommendation*: Start with JSON fields in DB (Phase 4), add S3 abstraction in Phase 11

7. **AI Context Window**: How much conversation history to send to AI?
   - *Recommendation*: Send last N messages + summary, implement in Phase 9

### 11.2 Architectural Consistency Check

✅ **Frontend→Backend**: Clear separation via REST API  
✅ **Backend→Database**: Services→Repositories→DB pattern enforced  
✅ **AI→Services**: Tools use services, not repositories directly  
✅ **Auth**: JWT on both frontend and backend  
✅ **Errors**: Consistent response format across API  
✅ **Types**: TypeScript strict mode on frontend, Pydantic on backend  
✅ **Async Patterns**: Redux Saga on frontend, async/await on backend  

---

## 12. Next Steps

### Immediate Actions:

1. ✅ Create repository structure
2. ✅ Initialize frontend (Vite, TypeScript, Tailwind)
3. ✅ Initialize backend (FastAPI, SQLAlchemy)
4. ✅ Create database models (Alembic migrations)
5. ✅ Configure environment files
6. ✅ Set up Docker Compose

### After Phase 0 Approval:

- Implement Phase 1 (Frontend Foundation)
- Implement Phase 2 (Backend Foundation)
- Proceed phase-by-phase with confirmation

---

## 13. Summary

This blueprint defines:

- ✅ Complete repository structure
- ✅ Full database schema with relationships
- ✅ REST API endpoints and response formats
- ✅ Redux store architecture with Saga patterns
- ✅ AI provider abstraction and tool design
- ✅ JWT authentication and RBAC authorization
- ✅ All environment variables
- ✅ Docker composition
- ✅ 12-phase development roadmap
- ✅ Architectural consistency checks
- ✅ Identified design decisions and open questions

**Status**: Ready for review and approval before Phase 1 implementation.
