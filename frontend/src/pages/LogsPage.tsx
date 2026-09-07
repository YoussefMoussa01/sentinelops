import { useEffect, useState } from 'react'
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

  return <div>
    <h1 className="mb-6 text-3xl font-bold text-gray-900">Logs</h1>
    <form onSubmit={search} className="mb-6 flex gap-3"><input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Search source, level or message" className="flex-1 rounded border border-gray-300 px-3 py-2" /><button type="submit" className="rounded bg-brand-600 px-4 py-2 font-medium text-white">Search</button></form>
    {loading && <p className="text-gray-600">Loading logs...</p>}{error && <p className="text-red-600">Unable to load logs: {error}</p>}
    {!loading && !error && <div className="overflow-hidden rounded-lg bg-white shadow"><div className="divide-y divide-gray-200">{logs.length === 0 ? <p className="p-6 text-gray-600">No logs found.</p> : logs.map((log) => <div key={log.id} className="p-5"><div className="flex justify-between gap-4"><span className="font-semibold text-gray-900">{log.level}</span><span className="text-sm text-gray-500">{log.source}</span></div><p className="mt-1 text-gray-700">{log.message}</p><p className="mt-2 text-xs text-gray-500">{log.event_time || 'No event time'}</p></div>)}</div></div>}
  </div>
}
