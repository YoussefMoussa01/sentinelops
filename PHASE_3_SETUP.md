# Phase 3: Authentication Setup Guide

## Overview
Phase 3 implements JWT-based authentication with login, logout, token refresh, and session restoration.

## Backend Setup

### 1. Environment Configuration
Create a `.env` file in the `backend/` directory:

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/sentinelops
JWT_SECRET_KEY=your-secret-key-change-this-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRATION_SECONDS=3600
JWT_REFRESH_EXPIRATION_SECONDS=604800
API_V1_PREFIX=/api/v1
API_TITLE=SentinelOps
API_VERSION=1.0.0
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
LOG_LEVEL=INFO
DEBUG=true
ENVIRONMENT=development
```

### 2. Database Setup
```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Initialize database tables
python init_db.py

# Seed initial test data
python seed_db.py
```

This creates two test users:
- **admin** / `AdminPassword123!`
- **investigator** / `InvestigatorPassword123!`

### 3. Start Backend Server
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: `http://localhost:8000`
API docs: `http://localhost:8000/docs`

## Frontend Setup

### 1. Environment Configuration
Create `.env.local` in the `frontend/` directory:

```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
VITE_TOKEN_STORAGE_KEY=sentinelops_token
```

### 2. Start Frontend Server
```bash
cd frontend
npm run dev
```

Frontend will be available at: `http://localhost:5173`

## Authentication Flow

### Login
1. User enters credentials on `/login` page
2. Frontend dispatches `loginRequest` action
3. Redux Saga calls `POST /api/v1/auth/login`
4. Backend validates credentials and returns tokens
5. Tokens stored in `localStorage`
6. Redux state updated, redirects to dashboard

### Session Restoration
1. App loads, `App.tsx` calls `restoreSessionRequest`
2. Saga retrieves token from localStorage
3. Saga calls `GET /api/v1/auth/me` with Bearer token
4. Backend validates token and returns user
5. Redux state restored, user stays logged in

### Logout
1. User clicks logout
2. Frontend dispatches `logoutRequest`
3. Saga calls `POST /api/v1/auth/logout`
4. Tokens cleared from localStorage
5. Redux state cleared, redirects to `/login`

### Token Refresh (Phase 3+)
1. Access token expires
2. API interceptor catches 401 response
3. Refresh token used to get new access token
4. Original request retried
5. User continues without interruption

## API Endpoints

### Authentication

**POST /auth/login**
```json
Request:
{
  "username": "admin",
  "password": "AdminPassword123!"
}

Response:
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "user": {
    "id": "uuid",
    "username": "admin",
    "email": "admin@sentinelops.local",
    "is_active": true,
    "created_at": "2026-08-18T10:00:00Z",
    "updated_at": "2026-08-18T10:00:00Z"
  }
}
```

**POST /auth/logout**
- Requires: Authorization Bearer token
- Response: `{"status": "success", "message": "Logged out successfully"}`

**GET /auth/me**
- Requires: Authorization Bearer token
- Response: User object

**POST /auth/refresh**
```json
Request:
{
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}

Response:
{
  "access_token": "new_token",
  "refresh_token": "new_refresh_token",
  "token_type": "bearer"
}
```

### Admin User Management

**GET /admin/users?page=1&page_size=20**
- Requires: Authorization Bearer token + admin permission
- Response: Paginated list of users

**POST /admin/users**
- Requires: Authorization Bearer token + admin permission
```json
Request:
{
  "username": "newuser",
  "email": "newuser@sentinelops.local",
  "password": "SecurePassword123!"
}
```

**PATCH /admin/users/{user_id}**
- Requires: Authorization Bearer token + admin permission
```json
Request:
{
  "email": "newemail@sentinelops.local",
  "is_active": true
}
```

**DELETE /admin/users/{user_id}**
- Requires: Authorization Bearer token + admin permission

## Testing

### Manual Testing
1. Open `http://localhost:5173` in browser
2. Go to `/login` page
3. Enter credentials: `admin` / `AdminPassword123!`
4. Should redirect to dashboard and show authenticated state
5. Refresh page - should restore session
6. Click logout - should redirect to login

### API Testing with curl
```bash
# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"AdminPassword123!"}'

# Get current user (replace TOKEN with access_token from login response)
curl -X GET http://localhost:8000/api/v1/auth/me \
  -H "Authorization: Bearer TOKEN"

# List users
curl -X GET http://localhost:8000/api/v1/admin/users \
  -H "Authorization: Bearer TOKEN"
```

## Troubleshooting

### "Invalid username or password"
- Check credentials in database: `python seed_db.py`
- Verify password is correctly hashed

### "Missing authorization header"
- Ensure frontend is sending: `Authorization: Bearer <token>`
- Check that token is stored in localStorage

### CORS errors
- Verify `CORS_ORIGINS` in backend `.env` includes frontend URL
- Restart backend after changing CORS settings

### Database connection errors
- Ensure PostgreSQL is running
- Check `DATABASE_URL` in `.env`
- Run `python init_db.py` to create tables

## Next Phase (Phase 4)
- Alerts management endpoints
- Investigation endpoints
- Permission-based access control
- Role management
