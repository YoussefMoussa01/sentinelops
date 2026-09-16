import { put, takeLatest, call } from 'redux-saga/effects'
import {
  loginRequest,
  loginSuccess,
  loginFailure,
  logoutRequest,
  logoutSuccess,
  restoreSessionRequest,
  restoreSessionSuccess,
  restoreSessionFailure,
} from '../state/authSlice'
import { apiClient } from '@/services/api/client'
import type { PayloadAction } from '@reduxjs/toolkit'
import type { LoginRequest, LoginResponse } from '../types/auth.types'

const TOKEN_KEY = import.meta.env.VITE_TOKEN_STORAGE_KEY || 'sentinelops_token'
const REFRESH_TOKEN_KEY = 'sentinelops_refresh_token'

function* loginSaga(action: PayloadAction<LoginRequest>): Generator<any, void, any> {
  try {
    // Call backend login endpoint
    const response: LoginResponse = yield call(() =>
      apiClient.post('/auth/login', {
        username: action.payload.username,
        password: action.payload.password,
      })
    )

    // Store tokens in localStorage
    localStorage.setItem(TOKEN_KEY, response.access_token)
    if (response.refresh_token) {
      localStorage.setItem(REFRESH_TOKEN_KEY, response.refresh_token)
    }

    // Dispatch success with user data
    yield put(
      loginSuccess({
        user: response.user,
        token: response.access_token,
        refreshToken: response.refresh_token,
      })
    )
  } catch (error) {
    const message = error instanceof Error ? error.message : 'Login failed'
    yield put(loginFailure(message))
  }
}

function* logoutSaga(): Generator<any, void, any> {
  try {
    // Call logout endpoint
    yield call(() => apiClient.post('/auth/logout', {}))

    // Clear tokens from localStorage
    localStorage.removeItem(TOKEN_KEY)
    localStorage.removeItem(REFRESH_TOKEN_KEY)

    yield put(logoutSuccess())
  } catch (error) {
    // Logout on client anyway
    localStorage.removeItem(TOKEN_KEY)
    localStorage.removeItem(REFRESH_TOKEN_KEY)
    yield put(logoutSuccess())
  }
}

function* restoreSessionSaga(): Generator<any, void, any> {
  try {
    const refreshToken = localStorage.getItem(REFRESH_TOKEN_KEY)

    // Renew first so a page refresh never starts with an expired access token.
    if (refreshToken) {
      const refreshed = yield call(() => apiClient.post('/auth/refresh', { refresh_token: refreshToken }))
      localStorage.setItem(TOKEN_KEY, refreshed.access_token)
      if (refreshed.refresh_token) localStorage.setItem(REFRESH_TOKEN_KEY, refreshed.refresh_token)
    }

    const token = localStorage.getItem(TOKEN_KEY)
    if (!token) {
      yield put(restoreSessionFailure())
      return
    }

    // Call /auth/me endpoint with token
    const response = yield call(() =>
      apiClient.get('/auth/me')
    )

    yield put(
      restoreSessionSuccess({
        user: response,
        token: localStorage.getItem(TOKEN_KEY) || token,
      })
    )
  } catch (error) {
    // Clear invalid tokens
    localStorage.removeItem(TOKEN_KEY)
    localStorage.removeItem(REFRESH_TOKEN_KEY)
    yield put(restoreSessionFailure())
  }
}

export default function* authSaga() {
  yield takeLatest(loginRequest.type, loginSaga)
  yield takeLatest(logoutRequest.type, logoutSaga)
  yield takeLatest(restoreSessionRequest.type, restoreSessionSaga)
}
