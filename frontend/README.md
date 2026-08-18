# SentinelOps Frontend

React + TypeScript + Vite + Redux Toolkit + Redux Saga

## Setup

```bash
cd frontend
npm install
cp .env.example .env
```

## Development

```bash
npm run dev
```

Server runs on http://localhost:5173

## Build

```bash
npm run build
```

## Structure

```
src/
├── app/
│   ├── store/           Redux setup (store.ts, hooks.ts, rootSaga.ts)
│   └── router/          Routes configuration
├── pages/               Page components
├── components/          Shared components (Layout, Header, Sidebar, etc.)
├── features/            Feature-based slices (auth, alerts, etc.)
│   └── auth/
│       ├── state/       Redux slice (authSlice.ts)
│       ├── sagas/       Side effects (authSagas.ts)
│       ├── types/       TypeScript types
│       └── hooks/       Custom hooks (useAuth)
├── hooks/               Shared hooks
├── services/            API clients
├── types/               Global types
├── data-types/          Domain model types
├── utils/               Utilities
└── App.tsx              Root component
```

## Redux + Saga Flow

```
Component
  ↓
dispatch(loginRequest(credentials))
  ↓
authSaga (watchLoginRequest)
  ↓
call(authAPI.login(credentials))
  ↓
API
  ↓
put(loginSuccess(data))
  ↓
authSlice reducer
  ↓
Redux state updates
  ↓
Component selector re-reads state
  ↓
Component re-renders
```

## Auth Hook

```tsx
const MyComponent = () => {
  const { user, isAuthenticated, login, logout } = useAuth()
  
  return (
    <>
      {isAuthenticated && <p>Welcome {user?.username}</p>}
      <button onClick={() => login({ username: 'john', password: 'pass' })}>
        Login
      </button>
    </>
  )
}
```

## Protected Routes

```tsx
<Route
  path="/alerts"
  element={
    <Layout>
      <ProtectedRoute 
        element={<AlertsPage />} 
        requiredPermission="view_alerts" 
      />
    </Layout>
  }
/>
```

## Environment Variables

Create `.env` (copy from `.env.example`):

```
VITE_API_BASE_URL=http://localhost:8000/api/v1
VITE_AUTH_REDIRECT_LOGIN=/login
VITE_AUTH_REDIRECT_DEFAULT=/dashboard
VITE_TOKEN_STORAGE_KEY=sentinelops_token
VITE_USER_STORAGE_KEY=sentinelops_user
```

## Notes

- **Phase 1**: Foundation (React, Redux, Saga, Routing, Layout)
- **Phase 3**: Authentication (JWT, login/logout, session restore)
- **Phase 4**: Security Domain (Alerts, Users, Devices)
- **Phase 7**: Advanced (Search, Filters, Pagination, URL state)

All API calls are stubbed for Phase 1. Will be connected in Phase 3+.
