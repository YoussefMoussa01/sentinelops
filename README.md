# SentinelOps — AI Cyber Investigation Platform

Production-style defensive cybersecurity investigation platform. Learning project focused on mastering React, Redux, FastAPI, PostgreSQL, and AI agents.

## Quick Start

### Prerequisites

- Node.js 20+
- Python 3.12+
- PostgreSQL 15+
- Docker & Docker Compose (optional)

### Option 1: Local Development

#### Frontend

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

Frontend: http://localhost:5173

#### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # macOS/Linux
# or: venv\Scripts\activate  # Windows
pip install -r requirements.txt
cp .env.example .env
```

Start PostgreSQL (ensure it's running on localhost:5432).

Then:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend: http://localhost:8000
API Docs: http://localhost:8000/docs

### Option 2: Docker Compose

```bash
docker-compose up
```

- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- PostgreSQL: localhost:5432

## Project Structure

```
sentinelops/
├── frontend/                React + TypeScript + Vite
│   ├── src/
│   │   ├── app/            Redux store + routing
│   │   ├── components/     Layout, Header, Sidebar
│   │   ├── features/       Redux slices (auth, alerts, etc.)
│   │   ├── pages/          Page components
│   │   ├── services/       API client
│   │   └── utils/          Helpers
│   ├── package.json
│   ├── vite.config.ts
│   ├── tsconfig.json
│   ├── tailwind.config.js
│   └── README.md
├── backend/                FastAPI + SQLAlchemy
│   ├── app/
│   │   ├── api/            v1 routes + dependencies
│   │   ├── models/         SQLAlchemy ORM models
│   │   ├── schemas/        Pydantic schemas
│   │   ├── repositories/   Data access layer
│   │   ├── services/       Business logic
│   │   ├── agents/         AI agents
│   │   ├── tools/          AI tools
│   │   ├── providers/      AI providers
│   │   ├── database/       DB config + migrations
│   │   ├── core/           Config, security, exceptions
│   │   ├── utils/          Helpers
│   │   └── main.py         FastAPI app
│   ├── requirements.txt
│   ├── alembic.ini
│   ├── Dockerfile
│   └── README.md
├── docker-compose.yml
├── Dockerfile.frontend
├── PHASE_0_BLUEPRINT.md     Architecture documentation
└── README.md                (this file)
```

## Stack

### Frontend

- **React 18** + TypeScript
- **Vite** bundler
- **Redux Toolkit** + **Redux Saga** state management
- **React Router** v6
- **Tailwind CSS** styling
- **Axios** HTTP client
- **React Hook Form** + **Zod** validation
- **Recharts** for data visualization
- **Lucide React** icons

### Backend

- **FastAPI** web framework
- **SQLAlchemy 2.0** ORM
- **Alembic** migrations
- **PostgreSQL 15** database
- **Pydantic** validation
- **Python-Jose** JWT
- **Passlib + Bcrypt** password hashing
- **CORS** support

### AI

- **OpenRouter** API
- Provider abstraction pattern
- Tool/function calling
- Conversation memory

### Infrastructure

- **Docker** + **Docker Compose**
- **Uvicorn** ASGI server
- **Nginx** reverse proxy (production)

## Architecture

### Frontend Flow

```
Component
  ↓
dispatch(action)
  ↓
Redux Saga
  ↓
API Call
  ↓
put(success/failure action)
  ↓
Redux Reducer
  ↓
State Update
  ↓
Component Re-render
```

### Backend Flow

```
REST API
  ↓
Route Handler
  ↓
Service (Business Logic)
  ↓
Repository (Data Access)
  ↓
SQLAlchemy ORM
  ↓
PostgreSQL
```

### AI Flow

```
User Query
  ↓
Agent (Process Query)
  ↓
Tool Calls (Authorized)
  ↓
Services (Business Logic)
  ↓
Database
  ↓
Results
  ↓
Response to User
```

## Development Phases

| Phase | Title | Status |
|-------|-------|--------|
| 0 | Architecture | ✅ Complete |
| 1 | Frontend Foundation | ✅ Complete |
| 2 | Backend Foundation | 🔄 Current |
| 3 | Authentication | ⏭️ Next |
| 4 | Security Domain | 📋 Planned |
| 5 | Dashboard | 📋 Planned |
| 6 | Investigation Workflow | 📋 Planned |
| 7 | Advanced React | 📋 Planned |
| 8 | AI Provider & Agent | 📋 Planned |
| 9 | AI Investigation | 📋 Planned |
| 10 | Real-Time | 📋 Planned |
| 11 | Testing & Production | 📋 Planned |

## Features

### Current (Phase 1-2)

- ✅ Project scaffolding
- ✅ React routing + layout
- ✅ Redux + Saga setup
- ✅ Auth slice (no backend yet)
- ✅ Protected routes
- ✅ FastAPI setup
- ✅ PostgreSQL integration
- ✅ SQLAlchemy ORM
- ✅ Exception handling
- ✅ CORS configuration
- ✅ Docker setup

### Upcoming (Phase 3+)

- 🔄 JWT Authentication
- 🔄 User management
- 🔄 Alerts & incidents
- 🔄 Investigations
- 🔄 Dashboard with real data
- 🔄 Search & filters
- 🔄 AI investigation agent
- 🔄 Real-time notifications

## Key Decisions

### Architecture

- **Repository Pattern**: Separation of data access from business logic
- **Redux + Saga**: Predictable async state management
- **JWT Authentication**: Stateless auth
- **Provider Abstraction**: AI provider flexibility
- **Docker**: Local development environment consistency

### Technologies

- **FastAPI** over Flask: Type safety, automatic docs, performance
- **SQLAlchemy** over raw SQL: ORM safety, migrations
- **Pydantic** over manual validation: Type checking, error messages
- **Redux Saga** over async/await in thunks: Clear side effect patterns
- **Tailwind** over CSS modules: Rapid styling, consistency

## Security

- ✅ Password hashing with bcrypt
- ✅ JWT token-based auth
- ✅ CORS protection
- ✅ SQL injection prevention (ORM)
- ✅ Role-based access control structure
- ⏳ Permission-based route guards (Phase 3)
- ⏳ Tool authorization in AI (Phase 8)

## Contributing

This is a learning project. Changes follow:

1. **Feature branches**: `feature/description`
2. **Clean commits**: One logical change per commit
3. **Type safety**: No `any` types (Python or TypeScript)
4. **Tests**: When applicable (Phase 11)

## Notes

- **Fictional Security Data**: This is a demo platform. All security data is fictional.
- **Development**: `DEBUG=True` in `.env` enables hot reload and detailed errors
- **Production**: Set `DEBUG=False`, use strong JWT secret, configure CORS properly
- **Database**: Migrations managed by Alembic (Phase 3+)

## Documentation

- [Phase 0 Blueprint](PHASE_0_BLUEPRINT.md) — Complete architecture
- [Frontend README](frontend/README.md) — React setup
- [Backend README](backend/README.md) — FastAPI setup

## License

MIT
