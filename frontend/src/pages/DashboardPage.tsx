import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { dashboardAPI } from '@/services/api'

interface DashboardStats {
  active_alerts: number
  open_investigations: number
  monitored_users: number
  devices: number
  recent_alerts: Array<{ id: string; title: string; severity: string; status: string; source?: string }>
  recent_investigations: Array<{ id: string; title: string; severity: string; status: string; risk_score: number }>
}

export const DashboardPage = () => {
  const [stats, setStats] = useState<DashboardStats | null>(null)
  const [error, setError] = useState('')

  useEffect(() => {
    dashboardAPI.getStats()
      .then((response) => setStats(response as DashboardStats))
      .catch((requestError: Error) => setError(requestError.message))
  }, [])

  if (error) return <p className="text-red-600">Unable to load dashboard: {error}</p>
  if (!stats) return <p className="text-gray-600">Loading dashboard...</p>

  return (
    <div>
      <h1 className="text-3xl font-bold text-gray-900 mb-6">Dashboard</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-sm font-medium text-gray-600">Active Alerts</h3>
          <p className="text-3xl font-bold text-brand-600 mt-2">{stats.active_alerts}</p>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-sm font-medium text-gray-600">Open Investigations</h3>
          <p className="text-3xl font-bold text-brand-600 mt-2">{stats.open_investigations}</p>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-sm font-medium text-gray-600">Monitored Users</h3>
          <p className="text-3xl font-bold text-brand-600 mt-2">{stats.monitored_users}</p>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-sm font-medium text-gray-600">Devices</h3>
          <p className="text-3xl font-bold text-brand-600 mt-2">{stats.devices}</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-bold text-gray-900 mb-4">Recent Alerts</h2>
          {stats.recent_alerts.length === 0 ? <p className="text-gray-600">No recent alerts.</p> : stats.recent_alerts.map((alert) => (
            <Link key={alert.id} to={`/alerts/${alert.id}`} className="block border-b border-gray-100 py-3 last:border-0 hover:bg-gray-50">
              <span className="font-medium text-gray-900">{alert.title}</span>
              <span className="ml-2 text-sm text-gray-500">{alert.severity} · {alert.status}</span>
            </Link>
          ))}
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-bold text-gray-900 mb-4">Investigation Timeline</h2>
          {stats.recent_investigations.length === 0 ? <p className="text-gray-600">No recent investigations.</p> : stats.recent_investigations.map((investigation) => (
            <Link key={investigation.id} to={`/investigations/${investigation.id}`} className="block border-b border-gray-100 py-3 last:border-0 hover:bg-gray-50">
              <span className="font-medium text-gray-900">{investigation.title}</span>
              <span className="ml-2 text-sm text-gray-500">{investigation.status} · Risk {investigation.risk_score}</span>
            </Link>
          ))}
        </div>
      </div>
    </div>
  )
}
