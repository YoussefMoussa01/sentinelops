import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { Sparkles, Trash2 } from 'lucide-react'
import { aiAPI, alertsAPI, investigationsAPI } from '@/services/api'
import { useAuth } from '@/features/auth/hooks/useAuth'

interface InvestigationDetails {
  id: string
  title: string
  description?: string
  severity: string
  status: string
  risk_score: number
  created_by?: string
  creator?: { id: string; username: string } | null
  assigned_to?: string
  assignee?: { id: string; username: string } | null
  created_at?: string
  updated_at?: string
}

interface AssigneeOption { id: string; username: string }

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
  details?: { from_status?: string; to_status?: string; changed_by?: string | null }
}

interface EvidenceItem { id: string; title: string; description?: string; evidence_type: string; source?: string; reference?: string; created_at: string }
interface NoteItem { id: string; content: string; created_at: string }

interface WorkflowToolCall { tool: string; status: string; error_message?: string | null; summary?: string | null }
interface WorkflowResult { workflow: string; answer: string; provider: string; tool_calls: WorkflowToolCall[]; generated_at?: string }

export const InvestigationDetailPage = () => {
  const { user } = useAuth()
  const canManageInvestigations = user?.permissions?.includes('manage_investigations') ?? false
  const canUseAI = user?.permissions?.includes('use_ai_agent') ?? false
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
  const [evidence, setEvidence] = useState<EvidenceItem[]>([])
  const [notes, setNotes] = useState<NoteItem[]>([])
  const [noteContent, setNoteContent] = useState('')
  const [evidenceTitle, setEvidenceTitle] = useState('')
  const [evidenceReference, setEvidenceReference] = useState('')
  const [resourceSaving, setResourceSaving] = useState(false)
  const [assignees, setAssignees] = useState<AssigneeOption[]>([])
  const [brief, setBrief] = useState<WorkflowResult | null>(null)
  const [briefing, setBriefing] = useState(false)
  const [briefError, setBriefError] = useState('')
  const [savingBrief, setSavingBrief] = useState(false)

  useEffect(() => {
    if (!investigationId) return

    investigationsAPI.getInvestigation(investigationId)
      .then((response) => setInvestigation(response as InvestigationDetails))
      .catch((requestError: Error) => setError(requestError.message))
      .finally(() => setLoading(false))
    if (canManageInvestigations) {
      investigationsAPI.getAssignees().then((response) => {
        if (Array.isArray(response)) setAssignees(response as AssigneeOption[])
      }).catch(() => setAssignees([]))
    }
    alertsAPI.getAlerts({ limit: 100 }).then((response) => {
      setAlerts(response.items as AlertItem[])
    }).catch(() => setAlerts([]))
    investigationsAPI.getInvestigationTimeline(investigationId).then((response) => {
      if (Array.isArray(response)) setTimeline(response as TimelineEvent[])
    })
    investigationsAPI.getEvidence(investigationId).then((response) => { if (Array.isArray(response)) setEvidence(response as EvidenceItem[]) })
    investigationsAPI.getNotes(investigationId).then((response) => { if (Array.isArray(response)) setNotes(response as NoteItem[]) })
  }, [investigationId])

  const addNote = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    if (!investigationId || !noteContent.trim()) return
    setResourceSaving(true)
    try {
      const created = await investigationsAPI.createNote(investigationId, { content: noteContent }) as NoteItem
      setNotes((current) => [created, ...current]); setNoteContent('')
    } catch (requestError) { setError(requestError instanceof Error ? requestError.message : 'Unable to add note') }
    finally { setResourceSaving(false) }
  }

  const addEvidence = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    if (!investigationId || !evidenceTitle.trim()) return
    setResourceSaving(true)
    try {
      const created = await investigationsAPI.createEvidence(investigationId, { title: evidenceTitle, reference: evidenceReference || undefined, evidence_type: 'REFERENCE' }) as EvidenceItem
      setEvidence((current) => [created, ...current]); setEvidenceTitle(''); setEvidenceReference('')
    } catch (requestError) { setError(requestError instanceof Error ? requestError.message : 'Unable to add evidence') }
    finally { setResourceSaving(false) }
  }

  const removeNote = async (noteId: string) => {
    if (!investigationId || !window.confirm('Delete this note?')) return
    try { await investigationsAPI.deleteNote(investigationId, noteId); setNotes((current) => current.filter((note) => note.id !== noteId)) }
    catch (requestError) { setError(requestError instanceof Error ? requestError.message : 'Unable to delete note') }
  }

  const removeEvidence = async (evidenceId: string) => {
    if (!investigationId || !window.confirm('Delete this evidence?')) return
    try { await investigationsAPI.deleteEvidence(investigationId, evidenceId); setEvidence((current) => current.filter((item) => item.id !== evidenceId)) }
    catch (requestError) { setError(requestError instanceof Error ? requestError.message : 'Unable to delete evidence') }
  }

  const runBrief = async () => {
    if (!investigationId) return
    setBriefing(true); setBriefError('')
    try { setBrief(await aiAPI.runInvestigationBrief(investigationId) as WorkflowResult) }
    catch (requestError) { setBriefError(requestError instanceof Error ? requestError.message : 'Unable to generate case brief') }
    finally { setBriefing(false) }
  }

  const saveBriefAsNote = async () => {
    if (!investigationId || !brief) return
    setSavingBrief(true)
    try {
      const created = await investigationsAPI.createNote(investigationId, { content: `AI case brief (${brief.provider})\n\n${brief.answer}` }) as NoteItem
      setNotes((current) => [created, ...current])
    } catch (requestError) { setBriefError(requestError instanceof Error ? requestError.message : 'Unable to save brief as note') }
    finally { setSavingBrief(false) }
  }

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
        assigned_to: form.get('assigned_to') || null,
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
    <div className="detail-shell space-y-6">
      <Link to="/investigations" className="text-sm font-semibold text-[var(--cyan)] hover:text-[var(--ink)]">Back to investigations</Link>
      <div className="page-hero rounded-2xl p-6 text-white md:p-8"><div className="relative z-10 flex flex-wrap items-end justify-between gap-5"><div><p className="eyebrow text-[var(--cyan)]">Case workspace</p><h1 className="mt-2 text-3xl font-bold tracking-tight md:text-4xl">{investigation?.title || 'Investigation details'}</h1><p className="mt-2 text-sm text-white/65">Review evidence, related alerts and the investigation timeline.</p></div>{investigation && <span className={`status-chip status-chip--${investigation.status.toLowerCase()}`}>{investigation.status}</span>}</div></div>
      {loading && <p className="text-gray-600">Loading investigation...</p>}
      {error && <p className="text-red-600">Unable to load investigation: {error}</p>}
      {!loading && !error && investigation && (
        <div className="detail-panel p-6 space-y-6">
          {canManageInvestigations && <div className="flex justify-end gap-3">
            <button onClick={() => setEditing(!editing)} className="btn-primary text-sm">{editing ? 'Cancel' : 'Edit'}</button>
            <button onClick={deleteInvestigation} className="btn-danger text-sm">Delete</button>
          </div>}
          {canManageInvestigations && editing && (
            <form onSubmit={updateInvestigation} className="space-y-4 border-b border-[var(--line)] pb-6">
              <input name="title" required defaultValue={investigation.title} className="field-control" />
              <textarea name="description" defaultValue={investigation.description} className="field-control" rows={3} />
              <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
                <select name="severity" defaultValue={investigation.severity} className="field-control"><option>LOW</option><option>MEDIUM</option><option>HIGH</option><option>CRITICAL</option></select>
                <input name="risk_score" type="number" min="0" max="100" step="0.1" defaultValue={investigation.risk_score} className="field-control" />
                <select name="status" defaultValue={investigation.status} className="field-control">{['OPEN', 'CLOSED', 'ARCHIVED'].map((status) => <option key={status}>{status}</option>)}</select>
                <select name="assigned_to" defaultValue={investigation.assigned_to || ''} className="field-control"><option value="">Unassigned</option>{assignees.map((assignee) => <option key={assignee.id} value={assignee.id}>{assignee.username}</option>)}</select>
              </div>
              <button disabled={saving} type="submit" className="btn-primary disabled:opacity-50">{saving ? 'Saving...' : 'Save changes'}</button>
            </form>
          )}
          <div className="flex flex-wrap items-start justify-between gap-4">
            <div>
              <h2 className="text-2xl font-semibold text-gray-900">{investigation.title}</h2>
              <p className="mt-2 text-gray-600">{investigation.description || 'No description'}</p>
            </div>
            <div className="text-right">
              <p className="font-semibold text-[var(--violet)]">Risk {investigation.risk_score}</p>
              <p className={`status-chip status-chip--${investigation.status.toLowerCase()}`}>{investigation.status}</p>
            </div>
          </div>
          <dl className="grid grid-cols-1 gap-4 border-t pt-5 sm:grid-cols-2">
            <div><dt className="text-sm text-gray-500">Severity</dt><dd className="mt-1 text-gray-900">{investigation.severity}</dd></div>
            <div><dt className="text-sm text-gray-500">Created by</dt><dd className="mt-1 text-gray-900">{investigation.creator?.username || investigation.created_by || 'Unknown'}</dd></div>
            <div><dt className="text-sm text-gray-500">Assignee</dt><dd className="mt-1 text-gray-900">{investigation.assignee?.username || 'Unassigned'}</dd></div>
            <div><dt className="text-sm text-gray-500">Created</dt><dd className="mt-1 text-gray-900">{investigation.created_at || 'Unknown'}</dd></div>
            <div><dt className="text-sm text-gray-500">Updated</dt><dd className="mt-1 text-gray-900">{investigation.updated_at || 'Unknown'}</dd></div>
          </dl>
          {canUseAI && <section className="border-t pt-5">
            <div className="flex flex-wrap items-center justify-between gap-3">
              <div><p className="eyebrow">Assisted analysis</p><h3 className="mt-1 text-lg font-semibold text-gray-900">AI case brief</h3><p className="mt-1 text-sm text-gray-500">Summarize this case from its alerts, evidence, notes and status history.</p></div>
              <button onClick={runBrief} disabled={briefing} className="btn-primary disabled:opacity-50"><Sparkles size={15} />{briefing ? 'Analyzing...' : 'Generate case brief'}</button>
            </div>
            {briefError && <p className="mt-3 text-sm text-red-700">Unable to generate brief: {briefError}</p>}
            {brief && <div className="mt-4 rounded-xl border border-[var(--line)] bg-slate-50/70 p-4">
              <div className="flex flex-wrap items-center gap-2"><span className="status-chip status-chip--low">{brief.provider}</span>{brief.tool_calls.filter((call) => call.status === 'SUCCESS').map((call) => <span key={call.tool} className="status-chip status-chip--low">{call.tool}</span>)}</div>
              <p className="mt-3 whitespace-pre-wrap text-sm leading-6 text-[var(--ink-soft)]">{brief.answer}</p>
              <div className="mt-3 flex flex-wrap items-center gap-3">{canManageInvestigations && <button onClick={saveBriefAsNote} disabled={savingBrief} className="btn-secondary disabled:opacity-50">{savingBrief ? 'Saving...' : 'Save brief as note'}</button>}{brief.generated_at && <span className="font-mono text-[10px] text-[var(--muted)]">{brief.generated_at}</span>}</div>
            </div>}
          </section>}
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
            {canManageInvestigations && <form onSubmit={linkAlert} className="mt-4 flex flex-wrap gap-3">
              <select value={selectedAlertId} onChange={(event) => setSelectedAlertId(event.target.value)} className="min-w-64 rounded border border-gray-300 px-3 py-2">
                <option value="">Select an alert to link</option>
                {alerts.filter((alert) => !alert.investigation_id).map((alert) => (
                  <option key={alert.id} value={alert.id}>{alert.title} ({alert.severity})</option>
                ))}
              </select>
              <button disabled={!selectedAlertId || linking} type="submit" className="rounded bg-brand-600 px-4 py-2 text-white disabled:opacity-50">{linking ? 'Linking...' : 'Link alert'}</button>
            </form>}
          </section>
          <div className="grid grid-cols-1 gap-6 border-t border-[var(--line)] pt-6 lg:grid-cols-2">
            <section>
              <div className="flex items-center justify-between"><div><p className="eyebrow">Case record</p><h3 className="mt-1 text-lg font-semibold text-[var(--ink)]">Investigation notes</h3></div><span className="status-chip status-chip--low">{notes.length}</span></div>
              {canManageInvestigations && <form onSubmit={addNote} className="mt-4 space-y-3"><textarea value={noteContent} onChange={(event) => setNoteContent(event.target.value)} placeholder="Record an observation or next step..." rows={3} className="field-control" /><button disabled={resourceSaving || !noteContent.trim()} type="submit" className="btn-primary disabled:opacity-50">Add note</button></form>}
              <div className="mt-4 space-y-3">{notes.length === 0 ? <p className="text-sm text-[var(--muted)]">No notes recorded yet.</p> : notes.map((note) => <article key={note.id} className="rounded-xl border border-[var(--line)] bg-slate-50/70 p-3"><div className="flex justify-between gap-3"><p className="text-sm leading-6 text-[var(--ink-soft)]">{note.content}</p>{canManageInvestigations && <button aria-label="Delete note" onClick={() => removeNote(note.id)} className="text-gray-400 hover:text-red-600"><Trash2 size={15} /></button>}</div><p className="mt-2 font-mono text-[10px] text-[var(--muted)]">{note.created_at}</p></article>)}</div>
            </section>
            <section>
              <div className="flex items-center justify-between"><div><p className="eyebrow">Collected material</p><h3 className="mt-1 text-lg font-semibold text-[var(--ink)]">Evidence</h3></div><span className="status-chip status-chip--low">{evidence.length}</span></div>
              {canManageInvestigations && <form onSubmit={addEvidence} className="mt-4 space-y-3"><input required value={evidenceTitle} onChange={(event) => setEvidenceTitle(event.target.value)} placeholder="Evidence title" className="field-control" /><input value={evidenceReference} onChange={(event) => setEvidenceReference(event.target.value)} placeholder="Reference, URL or case ID" className="field-control" /><button disabled={resourceSaving || !evidenceTitle.trim()} type="submit" className="btn-primary disabled:opacity-50">Add evidence</button></form>}
              <div className="mt-4 space-y-3">{evidence.length === 0 ? <p className="text-sm text-[var(--muted)]">No evidence collected yet.</p> : evidence.map((item) => <article key={item.id} className="rounded-xl border border-[var(--line)] bg-slate-50/70 p-3"><div className="flex justify-between gap-3"><p className="font-semibold text-[var(--ink)]">{item.title}</p>{canManageInvestigations && <button aria-label="Delete evidence" onClick={() => removeEvidence(item.id)} className="text-gray-400 hover:text-red-600"><Trash2 size={15} /></button>}</div><p className="mt-1 text-xs text-[var(--muted)]">{item.reference || 'No reference'} - {item.evidence_type}</p></article>)}</div>
            </section>
          </div>
          <section className="border-t pt-5">
            <h3 className="text-lg font-semibold text-gray-900">Investigation timeline</h3>
            <div className="mt-4 space-y-4 border-l-2 border-gray-200 pl-5">
              {timeline.map((event) => (
                <div key={`${event.type}-${event.timestamp}`} className="relative">
                  <span className="absolute -left-[1.6rem] top-1 h-3 w-3 rounded-full bg-brand-600" />
                  <p className="text-sm font-medium text-gray-900">{event.title}</p>
                  <p className="text-sm text-gray-600">{event.description}</p>
                  {event.details && <p className="mt-1 text-xs text-[var(--muted)]">Previous: {event.details.from_status} · New: {event.details.to_status}</p>}
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
