# SentinelOps Backend

Python 3.12 + FastAPI + PostgreSQL + SQLAlchemy + Alembic

## Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/Scripts/activate  # Windows
source venv/bin/activate      # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Copy environment
cp .env.example .env

# Initialize database (Phase 3)
# alembic upgrade head
```

## Development

```bash
# Start FastAPI server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Server runs on http://localhost:8000

API docs: http://localhost:8000/docs

## Database

PostgreSQL 15+

**Connection String**:
```
postgresql://sentinelops:sentinelops_pass@localhost:5432/sentinelops_db
```

### Migrations

Create first migration after models are defined (Phase 3+):

```bash
alembic revision --autogenerate -m "Initial schema"
alembic upgrade head
```

## Project Structure

```
app/
├── api/
│   ├── v1/                  API routes (v1)
│   ├── dependencies.py      Auth, permissions, DB
│   └── exceptions.py        Exception handlers
├── models/
│   ├── base.py              Base model with timestamps
│   ├── identity.py          User, Role, Permission
│   └── [domain].py          Security, Activity, etc. (Phase 4+)
├── schemas/
│   ├── common.py            Base schemas
│   ├── auth.py              Auth schemas
│   └── [domain].py          Domain schemas (Phase 4+)
├── repositories/
│   ├── user_repository.py   User CRUD
│   └── [domain].py          Domain repos (Phase 4+)
├── services/
│   ├── [domain]_service.py  Business logic (Phase 3+)
├── agents/
│   ├── security_agent.py    AI agent (Phase 8)
├── tools/
│   ├── [tool]_tool.py       AI tools (Phase 8)
├── providers/
│   ├── openrouter.py        OpenRouter provider (Phase 8)
├── database/
│   ├── session.py           SQLAlchemy setup
│   └── migrations/          Alembic migrations
├── core/
│   ├── config.py            Settings
│   ├── security.py          JWT, password hashing
│   ├── exceptions.py        Custom exceptions
│   ├── logging.py           Logger setup
│   └── constants.py         Enums and constants
├── utils/
│   ├── pagination.py        Pagination helpers
│   └── validators.py        Input validation
└── main.py                  FastAPI app entry point
```

## Configuration

### Environment Variables

`.env` file (copied from `.env.example`):

```
DATABASE_URL=postgresql://sentinelops:sentinelops_pass@localhost:5432/sentinelops_db
JWT_SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256
JWT_EXPIRATION_SECONDS=3600
JWT_REFRESH_EXPIRATION_SECONDS=604800
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
AI_PROVIDER=openrouter
OPENROUTER_API_KEY=
AI_MODEL=openai/gpt-4
DEBUG=True
ENVIRONMENT=development
```

## API Response Format

All successful responses:
```json
{
  "status": "success",
  "data": { /* payload */ },
  "meta": { "timestamp": "2026-08-18T10:30:00Z" }
}
```

Error responses:
```json
{
  "status": "error",
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Input validation failed",
    "details": null
  },
  "meta": { "timestamp": "2026-08-18T10:30:00Z" }
}
```

## Architecture

### Repository Pattern
```
API → Service → Repository → Database
```

### AI Architecture
```
API → Agent → Tools → Services → Repository → Database
```

All tool calls are authorized and validated at the service layer.

## Commands

```bash
# Run server
uvicorn app.main:app --reload

# Create migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1

# Format code
black app/

# Lint code
pylint app/

# Run tests
pytest
```

## Phases

**Phase 2 (this)**: Backend foundation
- ✅ FastAPI setup
- ✅ SQLAlchemy ORM
- ✅ Database configuration
- ✅ Exception handling
- ✅ CORS
- ✅ Logging
- ✅ Health check

**Phase 3**: Authentication
- User model complete
- JWT login/logout
- Session restoration
- Admin endpoints

**Phase 4**: Security Domain
- Alert model + API
- User/Device models + API
- Log models + API
- Investigation model + API

**Phase 8**: AI
- Provider abstraction
- Agent implementation
- Tool definitions
- OpenRouter integration

## Notes

- All API calls use consistent response format
- Proper error handling with custom exceptions
- Database sessions managed via dependency injection
- CORS configured for frontend communication
- Logging setup with rotating file handlers
- Password hashing with bcrypt
- JWT token generation and validation
