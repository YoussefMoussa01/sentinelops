# Phase 3: Quick Reference

## Test Credentials
```
Username: admin
Password: AdminPassword123!

OR

Username: investigator  
Password: InvestigatorPassword123!
```

## Backend Startup
```bash
cd backend

# Initialize database
python init_db.py

# Seed test data
python seed_db.py

# Start server
uvicorn app.main:app --reload --port 8000
```

## Frontend Startup
```bash
cd frontend
npm run dev
```

## URLs
- Frontend: http://localhost:5173
- Login: http://localhost:5173/login
- Backend API: http://localhost:8000/api/v1
- API Docs: http://localhost:8000/docs

## Key Endpoints

### Authentication
```
POST /auth/login
  Request: {"username": "admin", "password": "AdminPassword123!"}
  Response: {"access_token", "refresh_token", "user", "token_type"}

GET /auth/me
  Header: Authorization: Bearer <token>
  Response: {user data}

POST /auth/logout
  Header: Authorization: Bearer <token>
  Response: {"status": "success"}

POST /auth/refresh
  Request: {"refresh_token": "<token>"}
  Response: {"access_token", "refresh_token", "token_type"}
```

### Admin
```
GET /admin/users?page=1&page_size=20
  Header: Authorization: Bearer <token>
  Response: {users list with pagination}

POST /admin/users
  Header: Authorization: Bearer <token>
  Request: {"username", "email", "password"}
  Response: {created user}

PATCH /admin/users/{user_id}
  Header: Authorization: Bearer <token>
  Request: {"email", "is_active"}
  Response: {updated user}

DELETE /admin/users/{user_id}
  Header: Authorization: Bearer <token>
  Response: {"status": "success"}
```

## Environment Files

### Backend (.env)
```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/sentinelops
JWT_SECRET_KEY=your-secret-key-change-this
JWT_ALGORITHM=HS256
JWT_EXPIRATION_SECONDS=3600
JWT_REFRESH_EXPIRATION_SECONDS=604800
API_V1_PREFIX=/api/v1
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
DEBUG=true
```

### Frontend (.env.local)
```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
VITE_TOKEN_STORAGE_KEY=sentinelops_token
```

## Testing Flow

1. Navigate to http://localhost:5173/login
2. Enter credentials (admin / AdminPassword123!)
3. Click Sign In
4. Should redirect to /dashboard
5. Check localStorage - should have sentinelops_token
6. Refresh page - should stay logged in
7. Click logout - should redirect to /login

## Debugging

### Check tokens in browser
```javascript
// In browser console
localStorage.getItem('sentinelops_token')
localStorage.getItem('sentinelops_refresh_token')
```

### Test API with curl
```bash
# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"AdminPassword123!"}'

# Get current user
curl -X GET http://localhost:8000/api/v1/auth/me \
  -H "Authorization: Bearer <token_from_login>"
```

## What's Implemented
✅ JWT authentication with access + refresh tokens
✅ Password hashing with bcrypt
✅ Session restoration
✅ Bearer token authorization
✅ Admin user management
✅ Error handling and validation
✅ CORS support
✅ Database migrations
✅ Redux Saga integration
✅ API interceptors

## Phase 4 Next Steps
- Alerts CRUD endpoints
- Investigation endpoints
- Permission-based access control
- Role assignment
- Advanced filtering and search
