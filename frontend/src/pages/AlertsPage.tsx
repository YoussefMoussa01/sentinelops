import { useCallback, useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { ArrowDown, ArrowUp, Plus, Search } from 'lucide-react'
import { alertsAPI, devicesAPI } from '@/services/api'
import { useAuth } from '@/features/auth/hooks/useAuth'
import { useListQuery } from '@/hooks/useListQuery'

interface AlertItem {
  id: string
  title: string
  description?: string
  severity: string
  status: string
  source?: string
  detection_time?: string
  device_id?: string
  device?: { hostname: string; ip_address?: string; status: string }
}

interface DeviceOption {
  id: string
  hostname: string
  ip_address?: string
  status: string
}

const SORT_OPTIONS = [
  { value: 'created_at', label: 'Created' },
  { value: 'severity', label: 'Severity' },
  { value: 'status', label: 'Status' },
  { value: 'title', label: 'Title' },
]

export const AlertsPage = () => {
  const { user } = useAuth()
  const canManageAlerts = user?.permissions?.includes('manage_alerts') ?? false
  const { filters, searchInput, setSearch, setStatus, setSeverity, setPage, toggleSort, pageSize } = useListQuery({
    defaultSortBy: 'created_at',
    defaultSortDir: 'desc',
  })
  const [alerts, setAlerts] = useState<AlertItem[]>([])
  const [total, setTotal] = useState(0)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [showForm, setShowForm] = useState(false)
  const [title, setTitle] = useState('')
  const [description, setDescription] = useState('')
  const [severity, setSeverityValue] = useState('MEDIUM')
  const [source, setSource] = useState('')
  const [saving, setSaving] = useState(false)
  const [devices, setDevices] = useState<DeviceOption[]>([])
  const [deviceId, setDeviceId] = useState('')

  const loadAlerts = useCallback(() => {
    setLoading(true)
    alertsAPI.getAlerts({
      skip: filters.page * pageSize,
      limit: pageSize,
      search: filters.search || undefined,
      status: filters.status === 'ALL' ? undefined : filters.status,
      severity: filters.severity === 'ALL' ? undefined : filters.severity,
      sort_by: filters.sortBy,
      sort_dir: filters.sortDir,
    })
      .then((response) => {
        setAlerts(response.items as AlertItem[])
        setTotal(response.total)
      })
      .catch((requestError: Error) => setError(requestError.message))
      .finally(() => setLoading(false))
  }, [filters.page, filters.search, filters.status, filters.severity, filters.sortBy, filters.sortDir, pageSize])

  useEffect(() => {
    loadAlerts()
  }, [loadAlerts])

  useEffect(() => {
    devicesAPI.getDevices().then((response) => {
      if (Array.isArray(response)) setDevices(response as DeviceOption[])
    }).catch(() => setDevices([]))
  }, [])

  const createAlert = async (event: React.FormEvent) => {
    event.preventDefault()
    setSaving(true)
    setError('')
    try {
      await alertsAPI.createAlert({ title, description, severity, source, device_id: deviceId || null })
      setTitle('')
      setDescription('')
      setSource('')
      setDeviceId('')
      setShowForm(false)
      if (filters.page !== 0) setPage(0)
      else loadAlerts()
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : 'Unable to create alert')
    } finally {
      setSaving(false)
    }
  }

  const totalPages = Math.max(1, Math.ceil(total / pageSize))

  return (
    <div className="page-frame space-y-6">
      <div className="flex flex-wrap items-center justify-between gap-4 mb-6">
        <div><p className="eyebrow">Signal triage</p><h1 className="mt-2 text-3xl font-bold tracking-tight text-[var(--ink)]">Alerts</h1><p className="mt-2 text-sm text-[var(--muted)]">Review active signals and move the right events into investigation.</p></div>
        {canManageAlerts && <button onClick={() => setShowForm(!showForm)} className="btn-primary">
          <Plus size={17} />
          {showForm ? 'Cancel' : 'New alert'}
        </button>}
      </div>
      {canManageAlerts && showForm && (
        <form onSubmit={createAlert} className="surface rounded-2xl p-6 space-y-4">
          <div><p className="eyebrow">Create signal</p><h2 className="mt-1 text-xl font-bold">Add an alert to the triage queue</h2></div>
          <input required value={title} onChange={(event) => setTitle(event.target.value)} placeholder="Alert title" className="field-control" />
          <textarea value={description} onChange={(event) => setDescription(event.target.value)} placeholder="Description" className="field-control" rows={3} />
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <select value={severity} onChange={(event) => setSeverityValue(event.target.value)} className="field-control">
              <option>LOW</option><option>MEDIUM</option><option>HIGH</option><option>CRITICAL</option>
            </select>
            <div>
              <select value={source} onChange={(event) => setSource(event.target.value)} className="field-control">
                <option value="">Select source</option>
                <option value="EDR">EDR</option>
                <option value="Firewall">Firewall</option>
                <option value="SIEM">SIEM</option>
                <option value="Microsoft Defender">Microsoft Defender</option>
                <option value="Windows Event Log">Windows Event Log</option>
                <option value="IDS">IDS</option>
                <option value="Other">Other</option>
              </select>
              <p className="mt-1 text-xs text-gray-500">The system or tool that detected this alert.</p>
            </div>
            <div>
              <select value={deviceId} onChange={(event) => setDeviceId(event.target.value)} className="field-control">
                <option value="">No device linked</option>
                {devices.map((device) => <option key={device.id} value={device.id}>{device.hostname} · {device.ip_address || 'No IP'} · {device.status}</option>)}
              </select>
              <p className="mt-1 text-xs text-gray-500">Link the alert to a monitored device. Its IP stays managed on the device.</p>
            </div>
          </div>
          <button disabled={saving} type="submit" className="btn-primary disabled:opacity-50">
            {saving ? 'Creating...' : 'Create alert'}
          </button>
        </form>
      )}
      {error && <p className="text-red-600">Unable to load alerts: {error}</p>}
      {!error && (
        <div className="surface overflow-hidden rounded-2xl">
          <div className="grid grid-cols-1 gap-3 border-b border-[var(--line)] bg-slate-50/70 p-4 md:grid-cols-2 lg:grid-cols-4">
            <label className="relative"><Search size={16} className="absolute left-3 top-3 text-[var(--muted)]" /><input value={searchInput} onChange={(event) => setSearch(event.target.value)} placeholder="Search alerts" className="field-control pl-9" /></label>
            <select value={filters.status} onChange={(event) => setStatus(event.target.value)} className="field-control"><option value="ALL">All statuses</option><option>NEW</option><option>ACKNOWLEDGED</option><option>INVESTIGATING</option><option>RESOLVED</option><option>FALSE_POSITIVE</option></select>
            <select value={filters.severity} onChange={(event) => setSeverity(event.target.value)} className="field-control"><option value="ALL">All severities</option><option>LOW</option><option>MEDIUM</option><option>HIGH</option><option>CRITICAL</option></select>
            <div className="flex gap-2">
              <select value={filters.sortBy} onChange={(event) => toggleSort(event.target.value)} className="field-control" aria-label="Sort alerts by">{SORT_OPTIONS.map((option) => <option key={option.value} value={option.value}>Sort: {option.label}</option>)}</select>
              <button type="button" onClick={() => toggleSort(filters.sortBy)} aria-label="Toggle sort direction" className="btn-secondary px-3">{filters.sortDir === 'desc' ? <ArrowDown size={16} /> : <ArrowUp size={16} />}</button>
            </div>
          </div>
          {loading && <p className="p-6 text-gray-600">Loading alerts...</p>}
          {!loading && alerts.length === 0 && <p className="p-6 text-gray-600">No alerts found.</p>}
          {!loading && alerts.length > 0 && (
            <div className="divide-y divide-gray-200">
              {alerts.map((alert) => (
                <Link key={alert.id} to={`/alerts/${alert.id}`} className="data-row block p-5">
                  <div className="flex items-center justify-between gap-4">
                    <h2 className="font-semibold text-gray-900">{alert.title}</h2>
                    <span className={`status-chip status-chip--${alert.severity.toLowerCase()}`}>{alert.severity}</span>
                  </div>
                  <p className="mt-1 text-sm text-gray-600">{alert.description || 'No description'}</p>
                  <p className="mt-2 text-xs text-gray-500">{alert.status} {alert.source ? `· ${alert.source}` : ''} {alert.device ? `· ${alert.device.hostname} · ${alert.device.ip_address || 'No IP'}` : ''}</p>
                </Link>
              ))}
            </div>
          )}
          <div className="flex items-center justify-between border-t border-gray-200 p-4">
            <button disabled={filters.page === 0 || loading} onClick={() => setPage(filters.page - 1)} className="rounded border border-gray-300 px-3 py-2 text-sm disabled:opacity-40">Previous</button>
            <span className="text-sm text-gray-500">Page {filters.page + 1} of {totalPages} · {total} alerts</span>
            <button disabled={filters.page + 1 >= totalPages || loading} onClick={() => setPage(filters.page + 1)} className="rounded border border-gray-300 px-3 py-2 text-sm disabled:opacity-40">Next</button>
          </div>
        </div>
      )}
    </div>
  )
}
