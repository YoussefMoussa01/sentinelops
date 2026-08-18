import { createSlice, PayloadAction } from '@reduxjs/toolkit'
import { AuthState, User } from '../types/auth.types'

const initialState: AuthState = {
  isLoading: false,
  user: null,
  token: null,
  refreshToken: null,
  isAuthenticated: false,
  error: null,
}

const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    // Login
    loginRequest: (state) => {
      state.isLoading = true
      state.error = null
    },
    loginSuccess: (state, action: PayloadAction<{ user: User; token: string; refreshToken?: string }>) => {
      state.isLoading = false
      state.user = action.payload.user
      state.token = action.payload.token
      state.refreshToken = action.payload.refreshToken || null
      state.isAuthenticated = true
      state.error = null
    },
    loginFailure: (state, action: PayloadAction<string>) => {
      state.isLoading = false
      state.error = action.payload
      state.isAuthenticated = false
    },

    // Logout
    logoutRequest: (state) => {
      state.isLoading = true
    },
    logoutSuccess: (state) => {
      state.isLoading = false
      state.user = null
      state.token = null
      state.refreshToken = null
      state.isAuthenticated = false
      state.error = null
    },

    // Session restoration
    restoreSessionRequest: (state) => {
      state.isLoading = true
    },
    restoreSessionSuccess: (state, action: PayloadAction<{ user: User; token: string }>) => {
      state.isLoading = false
      state.user = action.payload.user
      state.token = action.payload.token
      state.isAuthenticated = true
      state.error = null
    },
    restoreSessionFailure: (state) => {
      state.isLoading = false
      state.user = null
      state.token = null
      state.isAuthenticated = false
    },

    // Token refresh
    refreshTokenRequest: (state) => {
      state.isLoading = true
    },
    refreshTokenSuccess: (state, action: PayloadAction<{ token: string; refreshToken?: string }>) => {
      state.isLoading = false
      state.token = action.payload.token
      if (action.payload.refreshToken) {
        state.refreshToken = action.payload.refreshToken
      }
      state.error = null
    },
    refreshTokenFailure: (state) => {
      state.isLoading = false
      state.token = null
      state.refreshToken = null
      state.isAuthenticated = false
    },

    // Clear error
    clearError: (state) => {
      state.error = null
    },
  },
})

export const {
  loginRequest,
  loginSuccess,
  loginFailure,
  logoutRequest,
  logoutSuccess,
  restoreSessionRequest,
  restoreSessionSuccess,
  restoreSessionFailure,
  refreshTokenRequest,
  refreshTokenSuccess,
  refreshTokenFailure,
  clearError,
} = authSlice.actions

export default authSlice.reducer

// Selectors
export const selectAuth = (state: { auth: AuthState }) => state.auth
export const selectIsAuthenticated = (state: { auth: AuthState }) => state.auth.isAuthenticated
export const selectUser = (state: { auth: AuthState }) => state.auth.user
export const selectToken = (state: { auth: AuthState }) => state.auth.token
export const selectAuthLoading = (state: { auth: AuthState }) => state.auth.isLoading
export const selectAuthError = (state: { auth: AuthState }) => state.auth.error
