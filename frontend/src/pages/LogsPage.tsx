import { useEffect, useState } from 'react'
import { Search, TerminalSquare } from 'lucide-react'
import { logsAPI } from '@/services/api'

interface LogEvent { id: string; level: string; source: string; message: string; event_time?: string }

export const LogsPage = () => {
  const [logs, setLogs] = useState<LogEvent[]>([])
  const [query, setQuery] = useState('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const loadLogs = (search = '') => {
    setLoading(true)
    const request = search ? logsAPI.searchLogs(search) : logsAPI.getLogs()
    request.then((response) => setLogs(Array.isArray(response) ? response as LogEvent[] : []))
      .catch((requestError: Error) => setError(requestError.message))
      .finally(() => setLoading(false))
  }

  useEffect(() => { loadLogs() }, [])
  const search = (event: React.FormEvent) => { event.preventDefault(); loadLogs(query) }

  return <div className="page-frame space-y-6">
    <div><p className="eyebrow">Activity stream</p><h1 className="mt-2 text-3xl font-bold tracking-tight text-[var(--ink)]">Logs</h1><p className="mt-2 text-sm text-[var(--muted)]">Search the events generated across your monitored environment.</p></div>
    <form onSubmit={search} className="surface flex gap-3 rounded-2xl p-4"><div className="relative min-w-0 flex-1"><Search size={16} className="absolute left-3 top-3 text-[var(--muted)]" /><input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Search source, level or message" className="field-control pl-9" /></div><button type="submit" className="btn-primary">Search</button></form>
    {loading && <p className="text-[var(--muted)]">Loading logs...</p>}{error && <p className="rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-700">Unable to load logs: {error}</p>}
    {!loading && !error && <div className="surface overflow-hidden rounded-2xl"><div className="divide-y divide-[var(--line)]">{logs.length === 0 ? <p className="p-6 text-[var(--muted)]">No logs found.</p> : logs.map((log) => <div key={log.id} className="data-row flex gap-4 p-5"><span className="mt-0.5 flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-slate-100 text-[var(--muted)]"><TerminalSquare size={15} /></span><div className="min-w-0 flex-1"><div className="flex flex-wrap justify-between gap-3"><span className={`status-chip status-chip--${log.level.toLowerCase()}`}>{log.level}</span><span className="text-xs font-medium text-[var(--muted)]">{log.source}</span></div><p className="mt-2 text-sm leading-6 text-[var(--ink-soft)]">{log.message}</p><p className="mt-2 font-mono text-[10px] text-[var(--muted)]">{log.event_time || 'No event time'}</p></div></div>)}</div></div>}
  </div>
}
