import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { alertsAPI } from '@/services/api'

interface AlertDetails {
  id: string
  title: string
  description?: string
  severity: string
  status: string
  source?: string
  detection_time?: string
  created_at?: string
  updated_at?: string
}

export const AlertDetailPage = () => {
  const { alertId } = useParams<{ alertId: string }>()
  const [alert, setAlert] = useState<AlertDetails | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [editing, setEditing] = useState(false)
  const [saving, setSaving] = useState(false)

  useEffect(() => {
    if (!alertId) return

    alertsAPI.getAlert(alertId)
      .then((response) => setAlert(response as AlertDetails))
      .catch((requestError: Error) => setError(requestError.message))
      .finally(() => setLoading(false))
  }, [alertId])

  const updateAlert = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    if (!alert || !alertId) return
    setSaving(true)
    setError('')
    const form = new FormData(event.currentTarget)
    try {
      const response = await alertsAPI.updateAlert(alertId, {
        title: form.get('title'), description: form.get('description'),
        severity: form.get('severity'), status: form.get('status'), source: form.get('source'),
      })
      setAlert({ ...alert, ...(response as Partial<AlertDetails>) })
      setEditing(false)
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : 'Unable to update alert')
    } finally {
      setSaving(false)
    }
  }

  const deleteAlert = async () => {
    if (!alertId || !window.confirm('Delete this alert?')) return
    try {
      await alertsAPI.deleteAlert(alertId)
      window.location.href = '/alerts'
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : 'Unable to delete alert')
    }
  }

  return (
    <div>
      <Link to="/alerts" className="text-sm text-brand-600 hover:underline">Back to alerts</Link>
      <h1 className="text-3xl font-bold text-gray-900 mt-3 mb-6">Alert Details</h1>
      {loading && <p className="text-gray-600">Loading alert...</p>}
      {error && <p className="text-red-600">Unable to load alert: {error}</p>}
      {!loading && !error && alert && (
        <div className="bg-white rounded-lg shadow p-6 space-y-5">
          <div className="flex justify-end gap-3">
            <button onClick={() => setEditing(!editing)} className="rounded border border-gray-300 px-3 py-2 text-sm">{editing ? 'Cancel' : 'Edit'}</button>
            <button onClick={deleteAlert} className="rounded bg-red-600 px-3 py-2 text-sm text-white hover:bg-red-700">Delete</button>
          </div>
          {editing && (
            <form onSubmit={updateAlert} className="space-y-4 border-b pb-5">
              <input name="title" required defaultValue={alert.title} className="w-full rounded border border-gray-300 px-3 py-2" />
              <textarea name="description" defaultValue={alert.description} className="w-full rounded border border-gray-300 px-3 py-2" rows={3} />
              <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
                <select name="severity" defaultValue={alert.severity} className="rounded border border-gray-300 px-3 py-2"><option>LOW</option><option>MEDIUM</option><option>HIGH</option><option>CRITICAL</option></select>
                <select name="status" defaultValue={alert.status} className="rounded border border-gray-300 px-3 py-2"><option>NEW</option><option>ACKNOWLEDGED</option><option>INVESTIGATING</option><option>RESOLVED</option><option>FALSE_POSITIVE</option></select>
                <input name="source" defaultValue={alert.source} placeholder="Source" className="rounded border border-gray-300 px-3 py-2" />
              </div>
              <button disabled={saving} type="submit" className="rounded bg-gray-900 px-4 py-2 text-white disabled:opacity-50">{saving ? 'Saving...' : 'Save changes'}</button>
            </form>
          )}
          <div className="flex flex-wrap items-start justify-between gap-4">
            <div>
              <h2 className="text-2xl font-semibold text-gray-900">{alert.title}</h2>
              <p className="mt-2 text-gray-600">{alert.description || 'No description'}</p>
            </div>
            <div className="text-right">
              <p className="font-semibold text-gray-900">{alert.severity}</p>
              <p className="text-sm text-gray-500">{alert.status}</p>
            </div>
          </div>
          <dl className="grid grid-cols-1 gap-4 border-t pt-5 sm:grid-cols-2">
            <div><dt className="text-sm text-gray-500">Source</dt><dd className="mt-1 text-gray-900">{alert.source || 'Unknown'}</dd></div>
            <div><dt className="text-sm text-gray-500">Detected</dt><dd className="mt-1 text-gray-900">{alert.detection_time || 'Unknown'}</dd></div>
            <div><dt className="text-sm text-gray-500">Created</dt><dd className="mt-1 text-gray-900">{alert.created_at || 'Unknown'}</dd></div>
            <div><dt className="text-sm text-gray-500">Updated</dt><dd className="mt-1 text-gray-900">{alert.updated_at || 'Unknown'}</dd></div>
          </dl>
        </div>
      )}
    </div>
  )
}
