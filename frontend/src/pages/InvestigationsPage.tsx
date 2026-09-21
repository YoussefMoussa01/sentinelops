import { useCallback, useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { ArrowDown, ArrowUp, ArrowUpRight, Plus, Search } from 'lucide-react'
import { investigationsAPI } from '@/services/api'
import { useAuth } from '@/features/auth/hooks/useAuth'
import { useListQuery } from '@/hooks/useListQuery'

interface InvestigationItem {
  id: string
  title: string
  description?: string
  severity: string
  status: string
  risk_score: number
  assignee?: { id: string; username: string } | null
}

const SORT_OPTIONS = [
  { value: 'created_at', label: 'Created' },
  { value: 'risk_score', label: 'Risk' },
  { value: 'severity', label: 'Severity' },
  { value: 'status', label: 'Status' },
  { value: 'title', label: 'Title' },
]

export const InvestigationsPage = () => {
  const { user } = useAuth()
  const canManageInvestigations = user?.permissions?.includes('manage_investigations') ?? false
  const { filters, searchInput, setSearch, setStatus, setSeverity, setPage, toggleSort, pageSize } = useListQuery({
    defaultSortBy: 'created_at',
    defaultSortDir: 'desc',
  })
  const [investigations, setInvestigations] = useState<InvestigationItem[]>([])
  const [total, setTotal] = useState(0)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [showForm, setShowForm] = useState(false)
  const [title, setTitle] = useState('')
  const [description, setDescription] = useState('')
  const [severity, setSeverityValue] = useState('MEDIUM')
  const [riskScore, setRiskScore] = useState('0')
  const [saving, setSaving] = useState(false)

  const loadInvestigations = useCallback(() => {
    setLoading(true)
    investigationsAPI.getInvestigations({
      skip: filters.page * pageSize,
      limit: pageSize,
      search: filters.search || undefined,
      status: filters.status === 'ALL' ? undefined : filters.status,
      severity: filters.severity === 'ALL' ? undefined : filters.severity,
      sort_by: filters.sortBy,
      sort_dir: filters.sortDir,
    })
      .then((response) => {
        setInvestigations(response.items as InvestigationItem[])
        setTotal(response.total)
      })
      .catch((requestError: Error) => setError(requestError.message))
      .finally(() => setLoading(false))
  }, [filters.page, filters.search, filters.status, filters.severity, filters.sortBy, filters.sortDir, pageSize])

  useEffect(() => {
    loadInvestigations()
  }, [loadInvestigations])

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
      if (filters.page !== 0) setPage(0)
      else loadInvestigations()
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : 'Unable to create investigation')
    } finally {
      setSaving(false)
    }
  }

  const totalPages = Math.max(1, Math.ceil(total / pageSize))

  return (
    <div className="page-frame space-y-6">
      <div className="flex flex-wrap items-center justify-between gap-4 mb-6">
        <div><p className="eyebrow">Case management</p><h1 className="mt-2 text-3xl font-bold tracking-tight text-[var(--ink)]">Investigations</h1><p className="mt-2 text-sm text-[var(--muted)]">Turn related signals into an auditable case with risk and a clear next action.</p></div>
        {canManageInvestigations && <button onClick={() => setShowForm(!showForm)} className="btn-primary"><Plus size={17} />
          {showForm ? 'Cancel' : 'New investigation'}
        </button>}
      </div>
      {canManageInvestigations && showForm && (
        <form onSubmit={createInvestigation} className="surface rounded-2xl p-6 space-y-4">
          <div><p className="eyebrow">Open a case</p><h2 className="mt-1 text-xl font-bold">Create an investigation workspace</h2></div>
          <input required value={title} onChange={(event) => setTitle(event.target.value)} placeholder="Investigation title" className="field-control" />
          <textarea value={description} onChange={(event) => setDescription(event.target.value)} placeholder="Description" className="field-control" rows={3} />
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <select value={severity} onChange={(event) => setSeverityValue(event.target.value)} className="field-control">
              <option>LOW</option><option>MEDIUM</option><option>HIGH</option><option>CRITICAL</option>
            </select>
            <input type="number" min="0" max="100" step="0.1" value={riskScore} onChange={(event) => setRiskScore(event.target.value)} placeholder="Risk score" className="field-control" />
          </div>
          <button disabled={saving} type="submit" className="btn-primary disabled:opacity-50">
            {saving ? 'Creating...' : 'Create investigation'}
          </button>
        </form>
      )}
      {error && <p className="text-red-600">Unable to load investigations: {error}</p>}
      {!error && (
        <div className="surface overflow-hidden rounded-2xl">
          <div className="grid grid-cols-1 gap-3 border-b border-[var(--line)] bg-slate-50/70 p-4 md:grid-cols-2 lg:grid-cols-4">
            <label className="relative"><Search size={16} className="absolute left-3 top-3 text-[var(--muted)]" /><input value={searchInput} onChange={(event) => setSearch(event.target.value)} placeholder="Search investigations" className="field-control pl-9" /></label>
            <select value={filters.status} onChange={(event) => setStatus(event.target.value)} className="field-control"><option value="ALL">All statuses</option><option>OPEN</option><option>CLOSED</option><option>ARCHIVED</option></select>
            <select value={filters.severity} onChange={(event) => setSeverity(event.target.value)} className="field-control"><option value="ALL">All severities</option><option>LOW</option><option>MEDIUM</option><option>HIGH</option><option>CRITICAL</option></select>
            <div className="flex gap-2">
              <select value={filters.sortBy} onChange={(event) => toggleSort(event.target.value)} className="field-control" aria-label="Sort investigations by">{SORT_OPTIONS.map((option) => <option key={option.value} value={option.value}>Sort: {option.label}</option>)}</select>
              <button type="button" onClick={() => toggleSort(filters.sortBy)} aria-label="Toggle sort direction" className="btn-secondary px-3">{filters.sortDir === 'desc' ? <ArrowDown size={16} /> : <ArrowUp size={16} />}</button>
            </div>
          </div>
          {loading && <p className="p-6 text-gray-600">Loading investigations...</p>}
          {!loading && investigations.length === 0 && <p className="p-6 text-gray-600">No investigations found.</p>}
          {!loading && investigations.length > 0 && (
            <div className="divide-y divide-gray-200">
              {investigations.map((investigation) => (
                <Link key={investigation.id} to={`/investigations/${investigation.id}`} className="data-row group block p-5">
                  <div className="flex items-center justify-between gap-4">
                    <h2 className="font-semibold text-gray-900">{investigation.title}</h2>
                    <span className="flex items-center gap-3 text-sm font-medium text-[var(--violet)]">Risk {investigation.risk_score}<ArrowUpRight size={15} className="opacity-0 transition group-hover:opacity-100" /></span>
                  </div>
                  <p className="mt-1 text-sm text-gray-600">{investigation.description || 'No description'}</p>
                  <p className="mt-2 text-xs text-gray-500">{investigation.status} · {investigation.severity} · {investigation.assignee?.username || 'Unassigned'}</p>
                </Link>
              ))}
            </div>
          )}
          <div className="flex items-center justify-between border-t border-gray-200 p-4">
            <button disabled={filters.page === 0 || loading} onClick={() => setPage(filters.page - 1)} className="rounded border border-gray-300 px-3 py-2 text-sm disabled:opacity-40">Previous</button>
            <span className="text-sm text-gray-500">Page {filters.page + 1} of {totalPages} · {total} investigations</span>
            <button disabled={filters.page + 1 >= totalPages || loading} onClick={() => setPage(filters.page + 1)} className="rounded border border-gray-300 px-3 py-2 text-sm disabled:opacity-40">Next</button>
          </div>
        </div>
      )}
    </div>
  )
}
