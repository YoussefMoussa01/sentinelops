import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { LoginPage } from '@/pages/LoginPage'
import { DashboardPage } from '@/pages/DashboardPage'
import { AlertsPage } from '@/pages/AlertsPage'
import { AlertDetailPage } from '@/pages/AlertDetailPage'
import { InvestigationsPage } from '@/pages/InvestigationsPage'
import { InvestigationDetailPage } from '@/pages/InvestigationDetailPage'
import { UsersPage } from '@/pages/UsersPage'
import { UserDetailPage } from '@/pages/UserDetailPage'
import { DevicesPage } from '@/pages/DevicesPage'
import { DeviceDetailPage } from '@/pages/DeviceDetailPage'
import { LogsPage } from '@/pages/LogsPage'
import { AiPage } from '@/pages/AiPage'
import { AdminPage } from '@/pages/AdminPage'
import { ProtectedRoute, Layout } from '@/components'

export const Router = () => (
  <BrowserRouter>
    <Routes>
      {/* Public routes */}
      <Route path="/login" element={<LoginPage />} />

      {/* Protected routes */}
      <Route
        path="/"
        element={
          <Layout>
            <Navigate to="/dashboard" replace />
          </Layout>
        }
      />
      <Route
        path="/dashboard"
        element={
          <Layout>
            <ProtectedRoute element={<DashboardPage />} />
          </Layout>
        }
      />
      <Route
        path="/alerts"
        element={
          <Layout>
            <ProtectedRoute element={<AlertsPage />} requiredPermission="view_alerts" />
          </Layout>
        }
      />
      <Route
        path="/alerts/:alertId"
        element={
          <Layout>
            <ProtectedRoute element={<AlertDetailPage />} requiredPermission="view_alerts" />
          </Layout>
        }
      />
      <Route
        path="/investigations"
        element={
          <Layout>
            <ProtectedRoute element={<InvestigationsPage />} />
          </Layout>
        }
      />
      <Route
        path="/investigations/:investigationId"
        element={
          <Layout>
            <ProtectedRoute element={<InvestigationDetailPage />} />
          </Layout>
        }
      />
      <Route
        path="/users"
        element={
          <Layout>
            <ProtectedRoute element={<UsersPage />} requiredPermission="view_users" />
          </Layout>
        }
      />
      <Route
        path="/users/:userId"
        element={
          <Layout>
            <ProtectedRoute element={<UserDetailPage />} requiredPermission="view_users" />
          </Layout>
        }
      />
      <Route
        path="/devices"
        element={
          <Layout>
            <ProtectedRoute element={<DevicesPage />} requiredPermission="view_users" />
          </Layout>
        }
      />
      <Route
        path="/devices/:deviceId"
        element={
          <Layout>
            <ProtectedRoute element={<DeviceDetailPage />} requiredPermission="view_users" />
          </Layout>
        }
      />
      <Route
        path="/logs"
        element={
          <Layout>
            <ProtectedRoute element={<LogsPage />} requiredPermission="view_logs" />
          </Layout>
        }
      />
      <Route
        path="/ai"
        element={
          <Layout>
            <ProtectedRoute element={<AiPage />} requiredPermission="use_ai_agent" />
          </Layout>
        }
      />
      <Route
        path="/admin"
        element={
          <Layout>
            <ProtectedRoute element={<AdminPage />} requiredPermission="manage_users" />
          </Layout>
        }
      />

      {/* 404 */}
      <Route
        path="*"
        element={
          <Layout>
            <div className="text-center py-12">
              <h1 className="text-4xl font-bold text-gray-900 mb-4">404</h1>
              <p className="text-gray-600">Page not found</p>
            </div>
          </Layout>
        }
      />
    </Routes>
  </BrowserRouter>
)
