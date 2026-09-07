import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { dashboardAPI } from '@/services/api'
import { Activity, AlertTriangle, ArrowUpRight, Bot, CircleDot, ShieldCheck, Users, Server } from 'lucide-react'

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

  const kpis = [
    { label: 'Active alerts', value: stats.active_alerts, detail: 'Requires triage', icon: AlertTriangle, color: 'text-[var(--coral)]', bg: 'bg-red-50' },
    { label: 'Open investigations', value: stats.open_investigations, detail: 'Cases in progress', icon: Activity, color: 'text-[var(--violet)]', bg: 'bg-violet-50' },
    { label: 'Monitored users', value: stats.monitored_users, detail: 'Active identities', icon: Users, color: 'text-[var(--cyan)]', bg: 'bg-teal-50' },
    { label: 'Devices', value: stats.devices, detail: 'Reporting assets', icon: Server, color: 'text-[var(--amber)]', bg: 'bg-amber-50' },
  ]

  return (
    <div className="space-y-8">
      <div className="flex flex-wrap items-end justify-between gap-4">
        <div><p className="eyebrow">Live posture</p><h1 className="mt-2 text-3xl font-bold tracking-tight text-[var(--ink)]">Command overview</h1><p className="mt-2 text-sm text-[var(--muted)]">A focused view of what needs attention across your environment.</p></div>
        <Link to="/ai" className="inline-flex items-center gap-2 rounded-lg bg-[var(--ink)] px-4 py-2.5 text-sm font-semibold text-white shadow-lg shadow-slate-900/10 hover:bg-[var(--cyan)]"><Bot size={17} /> Ask the agent <ArrowUpRight size={16} /></Link>
      </div>

      <div className="grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-4">
        {kpis.map(({ label, value, detail, icon: Icon, color, bg }) => <div key={label} className="surface rounded-xl p-5"><div className="flex items-start justify-between"><div className={`flex h-10 w-10 items-center justify-center rounded-lg ${bg} ${color}`}><Icon size={20} /></div><CircleDot size={16} className="text-[var(--line)]" /></div><p className="mt-5 text-sm font-medium text-[var(--muted)]">{label}</p><p className="mt-1 text-3xl font-bold tracking-tight text-[var(--ink)]">{value}</p><p className="mt-2 text-xs text-[var(--muted)]">{detail}</p></div>)}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="surface rounded-xl p-6">
          <div className="mb-3 flex items-center justify-between"><div><p className="eyebrow">Triage queue</p><h2 className="mt-1 text-xl font-bold text-[var(--ink)]">Recent alerts</h2></div><ShieldCheck className="text-[var(--cyan)]" size={21} /></div>
          {stats.recent_alerts.length === 0 ? <p className="text-gray-600">No recent alerts.</p> : stats.recent_alerts.map((alert) => (
            <Link key={alert.id} to={`/alerts/${alert.id}`} className="group flex items-center justify-between border-b border-gray-100 py-4 last:border-0 hover:bg-teal-50/40">
              <span><span className="block font-medium text-gray-900 group-hover:text-[var(--cyan)]">{alert.title}</span><span className="mt-1 block text-xs text-gray-500">{alert.source || 'Unknown source'}</span></span><span className="text-right text-sm text-gray-500">{alert.severity}<span className="block text-xs">{alert.status}</span></span>
            </Link>
          ))}
        </div>
        <div className="surface rounded-xl p-6">
          <div className="mb-3 flex items-center justify-between"><div><p className="eyebrow">Casework</p><h2 className="mt-1 text-xl font-bold text-[var(--ink)]">Investigation timeline</h2></div><Activity className="text-[var(--violet)]" size={21} /></div>
          {stats.recent_investigations.length === 0 ? <p className="text-gray-600">No recent investigations.</p> : stats.recent_investigations.map((investigation) => (
            <Link key={investigation.id} to={`/investigations/${investigation.id}`} className="group flex items-center justify-between border-b border-gray-100 py-4 last:border-0 hover:bg-violet-50/40">
              <span className="font-medium text-gray-900 group-hover:text-[var(--violet)]">{investigation.title}</span><span className="text-right text-sm text-gray-500">{investigation.status}<span className="block text-xs">Risk {investigation.risk_score}</span></span>
            </Link>
          ))}
        </div>
      </div>
    </div>
  )
}
