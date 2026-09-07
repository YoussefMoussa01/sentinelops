import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { ArrowUpRight, Plus, Search } from 'lucide-react'
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
  const [search, setSearch] = useState('')
  const [statusFilter, setStatusFilter] = useState('ALL')
  const [severityFilter, setSeverityFilter] = useState('ALL')
  const [page, setPage] = useState(0)
  const pageSize = 20

  useEffect(() => {
    loadInvestigations()
  }, [page])

  const loadInvestigations = () => {
    setLoading(true)
    investigationsAPI.getInvestigations(page * pageSize, pageSize)
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

  const filteredInvestigations = investigations.filter((investigation) => {
    const text = `${investigation.title} ${investigation.description || ''}`.toLowerCase()
    return text.includes(search.toLowerCase()) &&
      (statusFilter === 'ALL' || investigation.status === statusFilter) &&
      (severityFilter === 'ALL' || investigation.severity === severityFilter)
  })

  return (
    <div className="page-frame space-y-6">
      <div className="flex flex-wrap items-center justify-between gap-4 mb-6">
        <div><p className="eyebrow">Case management</p><h1 className="mt-2 text-3xl font-bold tracking-tight text-[var(--ink)]">Investigations</h1><p className="mt-2 text-sm text-[var(--muted)]">Turn related signals into an auditable case with risk and a clear next action.</p></div>
        <button onClick={() => setShowForm(!showForm)} className="btn-primary"><Plus size={17} />
          {showForm ? 'Cancel' : 'New investigation'}
        </button>
      </div>
      {showForm && (
        <form onSubmit={createInvestigation} className="surface rounded-2xl p-6 space-y-4">
          <div><p className="eyebrow">Open a case</p><h2 className="mt-1 text-xl font-bold">Create an investigation workspace</h2></div>
          <input required value={title} onChange={(event) => setTitle(event.target.value)} placeholder="Investigation title" className="field-control" />
          <textarea value={description} onChange={(event) => setDescription(event.target.value)} placeholder="Description" className="field-control" rows={3} />
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <select value={severity} onChange={(event) => setSeverity(event.target.value)} className="field-control">
              <option>LOW</option><option>MEDIUM</option><option>HIGH</option><option>CRITICAL</option>
            </select>
            <input type="number" min="0" max="100" step="0.1" value={riskScore} onChange={(event) => setRiskScore(event.target.value)} placeholder="Risk score" className="field-control" />
          </div>
          <button disabled={saving} type="submit" className="btn-primary disabled:opacity-50">
            {saving ? 'Creating...' : 'Create investigation'}
          </button>
        </form>
      )}
      {loading && <p className="text-gray-600">Loading investigations...</p>}
      {error && <p className="text-red-600">Unable to load investigations: {error}</p>}
      {!loading && !error && (
        <div className="surface overflow-hidden rounded-2xl">
          <div className="grid grid-cols-1 gap-3 border-b border-[var(--line)] bg-slate-50/70 p-4 md:grid-cols-3">
            <label className="relative"><Search size={16} className="absolute left-3 top-3 text-[var(--muted)]" /><input value={search} onChange={(event) => setSearch(event.target.value)} placeholder="Search investigations" className="field-control pl-9" /></label>
            <select value={statusFilter} onChange={(event) => setStatusFilter(event.target.value)} className="field-control"><option value="ALL">All statuses</option><option>OPEN</option><option>CLOSED</option><option>ARCHIVED</option></select>
            <select value={severityFilter} onChange={(event) => setSeverityFilter(event.target.value)} className="field-control"><option value="ALL">All severities</option><option>LOW</option><option>MEDIUM</option><option>HIGH</option><option>CRITICAL</option></select>
          </div>
          {filteredInvestigations.length === 0 ? (
            <p className="p-6 text-gray-600">No investigations found.</p>
          ) : (
            <div className="divide-y divide-gray-200">
              {filteredInvestigations.map((investigation) => (
                <Link key={investigation.id} to={`/investigations/${investigation.id}`} className="data-row group block p-5">
                  <div className="flex items-center justify-between gap-4">
                    <h2 className="font-semibold text-gray-900">{investigation.title}</h2>
                    <span className="flex items-center gap-3 text-sm font-medium text-[var(--violet)]">Risk {investigation.risk_score}<ArrowUpRight size={15} className="opacity-0 transition group-hover:opacity-100" /></span>
                  </div>
                  <p className="mt-1 text-sm text-gray-600">{investigation.description || 'No description'}</p>
                  <p className="mt-2 text-xs text-gray-500">{investigation.status} · {investigation.severity}</p>
                </Link>
              ))}
            </div>
          )}
          <div className="flex items-center justify-between border-t border-gray-200 p-4">
            <button disabled={page === 0 || loading} onClick={() => setPage(page - 1)} className="rounded border border-gray-300 px-3 py-2 text-sm disabled:opacity-40">Previous</button>
            <span className="text-sm text-gray-500">Page {page + 1}</span>
            <button disabled={investigations.length < pageSize || loading} onClick={() => setPage(page + 1)} className="rounded border border-gray-300 px-3 py-2 text-sm disabled:opacity-40">Next</button>
          </div>
        </div>
      )}
    </div>
  )
}
