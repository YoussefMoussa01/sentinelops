import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { alertsAPI } from '@/services/api'

interface AlertItem {
  id: string
  title: string
  description?: string
  severity: string
  status: string
  source?: string
  detection_time?: string
}

export const AlertsPage = () => {
  const [alerts, setAlerts] = useState<AlertItem[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [showForm, setShowForm] = useState(false)
  const [title, setTitle] = useState('')
  const [description, setDescription] = useState('')
  const [severity, setSeverity] = useState('MEDIUM')
  const [source, setSource] = useState('')
  const [saving, setSaving] = useState(false)

  useEffect(() => {
    loadAlerts()
  }, [])

  const loadAlerts = () => {
    setLoading(true)
    alertsAPI.getAlerts()
      .then((response) => {
        if (Array.isArray(response)) {
          setAlerts(response as AlertItem[])
          return
        }
        const payload = response as { data?: AlertItem[]; value?: AlertItem[] }
        setAlerts(payload.data || payload.value || [])
      })
      .catch((requestError: Error) => setError(requestError.message))
      .finally(() => setLoading(false))
  }

  const createAlert = async (event: React.FormEvent) => {
    event.preventDefault()
    setSaving(true)
    setError('')
    try {
      await alertsAPI.createAlert({ title, description, severity, source })
      setTitle('')
      setDescription('')
      setSource('')
      setShowForm(false)
      loadAlerts()
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : 'Unable to create alert')
    } finally {
      setSaving(false)
    }
  }

  return (
    <div>
      <div className="flex flex-wrap items-center justify-between gap-4 mb-6">
        <h1 className="text-3xl font-bold text-gray-900">Alerts</h1>
        <button onClick={() => setShowForm(!showForm)} className="rounded-lg bg-brand-600 px-4 py-2 font-medium text-white hover:bg-brand-700">
          {showForm ? 'Cancel' : 'New alert'}
        </button>
      </div>
      {showForm && (
        <form onSubmit={createAlert} className="bg-white rounded-lg shadow p-6 mb-6 space-y-4">
          <input required value={title} onChange={(event) => setTitle(event.target.value)} placeholder="Alert title" className="w-full rounded border border-gray-300 px-3 py-2" />
          <textarea value={description} onChange={(event) => setDescription(event.target.value)} placeholder="Description" className="w-full rounded border border-gray-300 px-3 py-2" rows={3} />
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <select value={severity} onChange={(event) => setSeverity(event.target.value)} className="rounded border border-gray-300 px-3 py-2">
              <option>LOW</option><option>MEDIUM</option><option>HIGH</option><option>CRITICAL</option>
            </select>
            <div>
              <select value={source} onChange={(event) => setSource(event.target.value)} className="w-full rounded border border-gray-300 px-3 py-2">
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
          </div>
          <button disabled={saving} type="submit" className="rounded-lg bg-gray-900 px-4 py-2 font-medium text-white disabled:opacity-50">
            {saving ? 'Creating...' : 'Create alert'}
          </button>
        </form>
      )}
      {loading && <p className="text-gray-600">Loading alerts...</p>}
      {error && <p className="text-red-600">Unable to load alerts: {error}</p>}
      {!loading && !error && (
        <div className="bg-white rounded-lg shadow overflow-hidden">
          {alerts.length === 0 ? (
            <p className="p-6 text-gray-600">No alerts found.</p>
          ) : (
            <div className="divide-y divide-gray-200">
              {alerts.map((alert) => (
                <Link key={alert.id} to={`/alerts/${alert.id}`} className="block p-5 hover:bg-gray-50">
                  <div className="flex items-center justify-between gap-4">
                    <h2 className="font-semibold text-gray-900">{alert.title}</h2>
                    <span className="text-sm font-medium text-gray-600">{alert.severity}</span>
                  </div>
                  <p className="mt-1 text-sm text-gray-600">{alert.description || 'No description'}</p>
                  <p className="mt-2 text-xs text-gray-500">{alert.status} {alert.source ? `· ${alert.source}` : ''}</p>
                </Link>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  )
}
