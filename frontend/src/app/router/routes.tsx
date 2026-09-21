import { lazy } from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { LoginPage } from '@/pages/LoginPage'
import { RegisterPage } from '@/pages/RegisterPage'
import { ProtectedRoute, Layout } from '@/components'

const DashboardPage = lazy(() => import('@/pages/DashboardPage').then((module) => ({ default: module.DashboardPage })))
const AlertsPage = lazy(() => import('@/pages/AlertsPage').then((module) => ({ default: module.AlertsPage })))
const AlertDetailPage = lazy(() => import('@/pages/AlertDetailPage').then((module) => ({ default: module.AlertDetailPage })))
const InvestigationsPage = lazy(() => import('@/pages/InvestigationsPage').then((module) => ({ default: module.InvestigationsPage })))
const InvestigationDetailPage = lazy(() => import('@/pages/InvestigationDetailPage').then((module) => ({ default: module.InvestigationDetailPage })))
const UsersPage = lazy(() => import('@/pages/UsersPage').then((module) => ({ default: module.UsersPage })))
const UserDetailPage = lazy(() => import('@/pages/UserDetailPage').then((module) => ({ default: module.UserDetailPage })))
const DevicesPage = lazy(() => import('@/pages/DevicesPage').then((module) => ({ default: module.DevicesPage })))
const DeviceDetailPage = lazy(() => import('@/pages/DeviceDetailPage').then((module) => ({ default: module.DeviceDetailPage })))
const LogsPage = lazy(() => import('@/pages/LogsPage').then((module) => ({ default: module.LogsPage })))
const IPAddressesPage = lazy(() => import('@/pages/IPAddressesPage').then((module) => ({ default: module.IPAddressesPage })))
const AiPage = lazy(() => import('@/pages/AiPage').then((module) => ({ default: module.AiPage })))
const AdminPage = lazy(() => import('@/pages/AdminPage').then((module) => ({ default: module.AdminPage })))

export const Router = () => (
  <BrowserRouter>
    <Routes>
      {/* Public routes */}
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />

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
            <ProtectedRoute element={<AlertsPage />} />
          </Layout>
        }
      />
      <Route
        path="/alerts/:alertId"
        element={
          <Layout>
            <ProtectedRoute element={<AlertDetailPage />} />
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
            <ProtectedRoute element={<DevicesPage />} requiredPermission="view_devices" />
          </Layout>
        }
      />
      <Route
        path="/devices/:deviceId"
        element={
          <Layout>
            <ProtectedRoute element={<DeviceDetailPage />} requiredPermission="view_devices" />
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
        path="/ip-addresses"
        element={
          <Layout>
            <ProtectedRoute element={<IPAddressesPage />} requiredPermission="view_ip_addresses" />
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
