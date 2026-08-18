import { useAppDispatch, useAppSelector } from '@/app/store/hooks'
import {
  selectIsAuthenticated,
  selectUser,
  selectAuthLoading,
  selectAuthError,
  loginRequest,
  logoutRequest,
  clearError,
} from '../state/authSlice'
import type { LoginRequest } from '../types/auth.types'

export const useAuth = () => {
  const dispatch = useAppDispatch()
  const isAuthenticated = useAppSelector(selectIsAuthenticated)
  const user = useAppSelector(selectUser)
  const isLoading = useAppSelector(selectAuthLoading)
  const error = useAppSelector(selectAuthError)

  const login = (credentials: LoginRequest) => {
    dispatch(loginRequest(credentials))
  }

  const logout = () => {
    dispatch(logoutRequest())
  }

  const clearAuthError = () => {
    dispatch(clearError())
  }

  return {
    isAuthenticated,
    user,
    isLoading,
    error,
    login,
    logout,
    clearAuthError,
  }
}
