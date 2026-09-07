import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { alertsAPI, investigationsAPI } from '@/services/api'

interface InvestigationDetails {
  id: string
  title: string
  description?: string
  severity: string
  status: string
  risk_score: number
  created_by?: string
  created_at?: string
  updated_at?: string
}

interface AlertItem {
  id: string
  title: string
  severity: string
  status: string
  investigation_id?: string
}

interface TimelineEvent {
  type: string
  title: string
  description: string
  timestamp: string
}

export const InvestigationDetailPage = () => {
  const { investigationId } = useParams<{ investigationId: string }>()
  const [investigation, setInvestigation] = useState<InvestigationDetails | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [editing, setEditing] = useState(false)
  const [saving, setSaving] = useState(false)
  const [alerts, setAlerts] = useState<AlertItem[]>([])
  const [selectedAlertId, setSelectedAlertId] = useState('')
  const [linking, setLinking] = useState(false)
  const [timeline, setTimeline] = useState<TimelineEvent[]>([])

  useEffect(() => {
    if (!investigationId) return

    investigationsAPI.getInvestigation(investigationId)
      .then((response) => setInvestigation(response as InvestigationDetails))
      .catch((requestError: Error) => setError(requestError.message))
      .finally(() => setLoading(false))
    alertsAPI.getAlerts().then((response) => {
      if (Array.isArray(response)) setAlerts(response as AlertItem[])
    })
    investigationsAPI.getInvestigationTimeline(investigationId).then((response) => {
      if (Array.isArray(response)) setTimeline(response as TimelineEvent[])
    })
  }, [investigationId])

  const linkAlert = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    if (!selectedAlertId || !investigationId) return
    setLinking(true)
    try {
      await alertsAPI.updateAlert(selectedAlertId, { investigation_id: investigationId })
      setAlerts((current) => current.map((alert) =>
        alert.id === selectedAlertId ? { ...alert, investigation_id: investigationId } : alert
      ))
      setSelectedAlertId('')
      const response = await investigationsAPI.getInvestigationTimeline(investigationId)
      if (Array.isArray(response)) setTimeline(response as TimelineEvent[])
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : 'Unable to link alert')
    } finally {
      setLinking(false)
    }
  }

  const updateInvestigation = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    if (!investigation || !investigationId) return
    setSaving(true)
    setError('')
    const form = new FormData(event.currentTarget)
    try {
      const response = await investigationsAPI.updateInvestigation(investigationId, {
        title: form.get('title'), description: form.get('description'),
        severity: form.get('severity'), status: form.get('status'), risk_score: Number(form.get('risk_score')),
      })
      setInvestigation({ ...investigation, ...(response as Partial<InvestigationDetails>) })
      setEditing(false)
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : 'Unable to update investigation')
    } finally {
      setSaving(false)
    }
  }

  const deleteInvestigation = async () => {
    if (!investigationId || !window.confirm('Delete this investigation?')) return
    try {
      await investigationsAPI.deleteInvestigation(investigationId)
      window.location.href = '/investigations'
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : 'Unable to delete investigation')
    }
  }

  return (
    <div>
      <Link to="/investigations" className="text-sm text-brand-600 hover:underline">Back to investigations</Link>
      <h1 className="text-3xl font-bold text-gray-900 mt-3 mb-6">Investigation Details</h1>
      {loading && <p className="text-gray-600">Loading investigation...</p>}
      {error && <p className="text-red-600">Unable to load investigation: {error}</p>}
      {!loading && !error && investigation && (
        <div className="bg-white rounded-lg shadow p-6 space-y-5">
          <div className="flex justify-end gap-3">
            <button onClick={() => setEditing(!editing)} className="rounded border border-gray-300 px-3 py-2 text-sm">{editing ? 'Cancel' : 'Edit'}</button>
            <button onClick={deleteInvestigation} className="rounded bg-red-600 px-3 py-2 text-sm text-white hover:bg-red-700">Delete</button>
          </div>
          {editing && (
            <form onSubmit={updateInvestigation} className="space-y-4 border-b pb-5">
              <input name="title" required defaultValue={investigation.title} className="w-full rounded border border-gray-300 px-3 py-2" />
              <textarea name="description" defaultValue={investigation.description} className="w-full rounded border border-gray-300 px-3 py-2" rows={3} />
              <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
                <select name="severity" defaultValue={investigation.severity} className="rounded border border-gray-300 px-3 py-2"><option>LOW</option><option>MEDIUM</option><option>HIGH</option><option>CRITICAL</option></select>
                <select name="status" defaultValue={investigation.status} className="rounded border border-gray-300 px-3 py-2"><option>OPEN</option><option>CLOSED</option><option>ARCHIVED</option></select>
                <input name="risk_score" type="number" min="0" max="100" step="0.1" defaultValue={investigation.risk_score} className="rounded border border-gray-300 px-3 py-2" />
              </div>
              <button disabled={saving} type="submit" className="rounded bg-gray-900 px-4 py-2 text-white disabled:opacity-50">{saving ? 'Saving...' : 'Save changes'}</button>
            </form>
          )}
          <div className="flex flex-wrap items-start justify-between gap-4">
            <div>
              <h2 className="text-2xl font-semibold text-gray-900">{investigation.title}</h2>
              <p className="mt-2 text-gray-600">{investigation.description || 'No description'}</p>
            </div>
            <div className="text-right">
              <p className="font-semibold text-gray-900">Risk {investigation.risk_score}</p>
              <p className="text-sm text-gray-500">{investigation.status}</p>
            </div>
          </div>
          <dl className="grid grid-cols-1 gap-4 border-t pt-5 sm:grid-cols-2">
            <div><dt className="text-sm text-gray-500">Severity</dt><dd className="mt-1 text-gray-900">{investigation.severity}</dd></div>
            <div><dt className="text-sm text-gray-500">Created by</dt><dd className="mt-1 text-gray-900">{investigation.created_by || 'Unknown'}</dd></div>
            <div><dt className="text-sm text-gray-500">Created</dt><dd className="mt-1 text-gray-900">{investigation.created_at || 'Unknown'}</dd></div>
            <div><dt className="text-sm text-gray-500">Updated</dt><dd className="mt-1 text-gray-900">{investigation.updated_at || 'Unknown'}</dd></div>
          </dl>
          <section className="border-t pt-5">
            <h3 className="text-lg font-semibold text-gray-900">Linked alerts</h3>
            <div className="mt-3 space-y-2">
              {alerts.filter((alert) => alert.investigation_id === investigation.id).map((alert) => (
                <Link key={alert.id} to={`/alerts/${alert.id}`} className="block rounded border border-gray-200 p-3 hover:bg-gray-50">
                  <span className="font-medium text-gray-900">{alert.title}</span>
                  <span className="ml-3 text-sm text-gray-500">{alert.severity} · {alert.status}</span>
                </Link>
              ))}
              {alerts.every((alert) => alert.investigation_id !== investigation.id) && <p className="text-sm text-gray-500">No alerts linked yet.</p>}
            </div>
            <form onSubmit={linkAlert} className="mt-4 flex flex-wrap gap-3">
              <select value={selectedAlertId} onChange={(event) => setSelectedAlertId(event.target.value)} className="min-w-64 rounded border border-gray-300 px-3 py-2">
                <option value="">Select an alert to link</option>
                {alerts.filter((alert) => !alert.investigation_id).map((alert) => (
                  <option key={alert.id} value={alert.id}>{alert.title} ({alert.severity})</option>
                ))}
              </select>
              <button disabled={!selectedAlertId || linking} type="submit" className="rounded bg-brand-600 px-4 py-2 text-white disabled:opacity-50">{linking ? 'Linking...' : 'Link alert'}</button>
            </form>
          </section>
          <section className="border-t pt-5">
            <h3 className="text-lg font-semibold text-gray-900">Investigation timeline</h3>
            <div className="mt-4 space-y-4 border-l-2 border-gray-200 pl-5">
              {timeline.map((event) => (
                <div key={`${event.type}-${event.timestamp}`} className="relative">
                  <span className="absolute -left-[1.6rem] top-1 h-3 w-3 rounded-full bg-brand-600" />
                  <p className="text-sm font-medium text-gray-900">{event.title}</p>
                  <p className="text-sm text-gray-600">{event.description}</p>
                  <p className="mt-1 text-xs text-gray-500">{event.timestamp}</p>
                </div>
              ))}
            </div>
          </section>
        </div>
      )}
    </div>
  )
}
