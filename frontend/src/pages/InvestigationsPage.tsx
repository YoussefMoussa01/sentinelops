import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { investigationsAPI } from '@/services/api'

interface InvestigationItem {
  id: string
  title: string
  description?: string
  severity: string
  status: string
  risk_score: number
}

export const InvestigationsPage = () => {
  const [investigations, setInvestigations] = useState<InvestigationItem[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [showForm, setShowForm] = useState(false)
  const [title, setTitle] = useState('')
  const [description, setDescription] = useState('')
  const [severity, setSeverity] = useState('MEDIUM')
  const [riskScore, setRiskScore] = useState('0')
  const [saving, setSaving] = useState(false)

  useEffect(() => {
    loadInvestigations()
  }, [])

  const loadInvestigations = () => {
    setLoading(true)
    investigationsAPI.getInvestigations()
      .then((response) => {
        if (Array.isArray(response)) {
          setInvestigations(response as InvestigationItem[])
          return
        }
        const payload = response as { data?: InvestigationItem[]; value?: InvestigationItem[] }
        setInvestigations(payload.data || payload.value || [])
      })
      .catch((requestError: Error) => setError(requestError.message))
      .finally(() => setLoading(false))
  }

  const createInvestigation = async (event: React.FormEvent) => {
    event.preventDefault()
    setSaving(true)
    setError('')
    try {
      await investigationsAPI.createInvestigation({
        title,
        description,
        severity,
        risk_score: Number(riskScore),
      })
      setTitle('')
      setDescription('')
      setRiskScore('0')
      setShowForm(false)
      loadInvestigations()
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : 'Unable to create investigation')
    } finally {
      setSaving(false)
    }
  }

  return (
    <div>
      <div className="flex flex-wrap items-center justify-between gap-4 mb-6">
        <h1 className="text-3xl font-bold text-gray-900">Investigations</h1>
        <button onClick={() => setShowForm(!showForm)} className="rounded-lg bg-brand-600 px-4 py-2 font-medium text-white hover:bg-brand-700">
          {showForm ? 'Cancel' : 'New investigation'}
        </button>
      </div>
      {showForm && (
        <form onSubmit={createInvestigation} className="bg-white rounded-lg shadow p-6 mb-6 space-y-4">
          <input required value={title} onChange={(event) => setTitle(event.target.value)} placeholder="Investigation title" className="w-full rounded border border-gray-300 px-3 py-2" />
          <textarea value={description} onChange={(event) => setDescription(event.target.value)} placeholder="Description" className="w-full rounded border border-gray-300 px-3 py-2" rows={3} />
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <select value={severity} onChange={(event) => setSeverity(event.target.value)} className="rounded border border-gray-300 px-3 py-2">
              <option>LOW</option><option>MEDIUM</option><option>HIGH</option><option>CRITICAL</option>
            </select>
            <input type="number" min="0" max="100" step="0.1" value={riskScore} onChange={(event) => setRiskScore(event.target.value)} placeholder="Risk score" className="rounded border border-gray-300 px-3 py-2" />
          </div>
          <button disabled={saving} type="submit" className="rounded-lg bg-gray-900 px-4 py-2 font-medium text-white disabled:opacity-50">
            {saving ? 'Creating...' : 'Create investigation'}
          </button>
        </form>
      )}
      {loading && <p className="text-gray-600">Loading investigations...</p>}
      {error && <p className="text-red-600">Unable to load investigations: {error}</p>}
      {!loading && !error && (
        <div className="bg-white rounded-lg shadow overflow-hidden">
          {investigations.length === 0 ? (
            <p className="p-6 text-gray-600">No investigations found.</p>
          ) : (
            <div className="divide-y divide-gray-200">
              {investigations.map((investigation) => (
                <Link key={investigation.id} to={`/investigations/${investigation.id}`} className="block p-5 hover:bg-gray-50">
                  <div className="flex items-center justify-between gap-4">
                    <h2 className="font-semibold text-gray-900">{investigation.title}</h2>
                    <span className="text-sm font-medium text-gray-600">Risk {investigation.risk_score}</span>
                  </div>
                  <p className="mt-1 text-sm text-gray-600">{investigation.description || 'No description'}</p>
                  <p className="mt-2 text-xs text-gray-500">{investigation.status} · {investigation.severity}</p>
                </Link>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  )
}
