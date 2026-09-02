import { ReactNode } from 'react'
import { Navigate } from 'react-router-dom'
import { useAuth } from '@/features/auth'

interface ProtectedRouteProps {
  element: ReactNode
  requiredRole?: string
  requiredPermission?: string
}

export const ProtectedRoute = ({
  element,
  requiredRole,
  requiredPermission,
}: ProtectedRouteProps) => {
  const { isAuthenticated, user } = useAuth()

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }

  if (requiredRole && (!user || !user.roles?.includes(requiredRole))) {
    return <Navigate to="/dashboard" replace />
  }

  if (requiredPermission && (!user || !user.permissions?.includes(requiredPermission))) {
    return <Navigate to="/dashboard" replace />
  }

  return <>{element}</>
}
