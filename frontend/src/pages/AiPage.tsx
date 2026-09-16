import { useEffect, useState } from 'react'
import { Archive, Bot, Clock3, MessageSquarePlus, Search, Send, ShieldAlert, Sparkles, Trash2 } from 'lucide-react'
import { aiAPI } from '@/services/api'
import { MarkdownMessage } from '@/components/MarkdownMessage'

interface Conversation { id: string; title: string; is_archived: boolean; updated_at: string }
interface StoredMessage { role: 'user' | 'assistant'; content: string }
interface ConversationDetails extends Conversation { messages: StoredMessage[] }

export const AiPage = () => {
  const [message, setMessage] = useState('')
  const [answer, setAnswer] = useState('')
  const [history, setHistory] = useState<string[]>([])
  const [conversationId, setConversationId] = useState<string | null>(null)
  const [conversations, setConversations] = useState<Conversation[]>([])
  const [showArchived, setShowArchived] = useState(false)
  const [search, setSearch] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const loadConversations = async (includeArchived = showArchived, query = search): Promise<Conversation[]> => {
    const response = await aiAPI.getConversations(includeArchived, query)
    const items = Array.isArray(response) ? response as Conversation[] : []
    setConversations(items)
    return items
  }

  const openConversation = async (id: string) => {
    setError('')
    try {
      const conversation = await aiAPI.getConversation(id) as ConversationDetails
      setConversationId(conversation.id)
      const latestAssistant = [...conversation.messages].reverse().find((item) => item.role === 'assistant')
      setAnswer(latestAssistant?.content || '')
      setHistory(conversation.messages.filter((item) => item.role === 'user').map((item) => item.content).slice(-4).reverse())
    } catch (requestError) { setError(requestError instanceof Error ? requestError.message : 'Unable to open conversation') }
  }

  const createConversation = async () => {
    const conversation = await aiAPI.createConversation({ title: 'AI investigation workspace' }) as ConversationDetails
    setConversationId(conversation.id)
    setAnswer('')
    setHistory([])
    await loadConversations()
  }

  useEffect(() => {
    loadConversations().then(async (items) => {
      if (items.length > 0) await openConversation(items[0].id)
      else await createConversation()
    }).catch((requestError) => setError(requestError instanceof Error ? requestError.message : 'Unable to load conversations'))
  }, [])

  const askAssistant = async (event: React.FormEvent) => {
    event.preventDefault()
    if (!message.trim() || loading) return
    setLoading(true); setError('')
    try {
      let activeConversationId = conversationId
      if (!activeConversationId) { const created = await aiAPI.createConversation({ title: 'AI investigation workspace' }) as Conversation; activeConversationId = created.id; setConversationId(activeConversationId) }
      const response = await aiAPI.sendMessage(activeConversationId, message) as { assistant_message: { content: string } }
      setAnswer(response.assistant_message.content)
      setHistory((current) => [message, ...current].slice(0, 4))
      setMessage('')
      await loadConversations()
    } catch (requestError) { setError(requestError instanceof Error ? requestError.message : 'Unable to contact assistant') }
    finally { setLoading(false) }
  }

  const archiveConversation = async (conversation: Conversation) => {
    try { await aiAPI.updateConversation(conversation.id, { is_archived: !conversation.is_archived }); await loadConversations(showArchived); if (conversation.id === conversationId) await createConversation() }
    catch (requestError) { setError(requestError instanceof Error ? requestError.message : 'Unable to update conversation') }
  }

  const deleteConversation = async (conversation: Conversation) => {
    if (!window.confirm('Delete this conversation permanently?')) return
    try { await aiAPI.deleteConversation(conversation.id); if (conversation.id === conversationId) { setConversationId(null); setAnswer(''); setHistory([]) }; await loadConversations(showArchived) }
    catch (requestError) { setError(requestError instanceof Error ? requestError.message : 'Unable to delete conversation') }
  }

  const prompts = ['Triage the highest risk alert', 'Summarize this investigation', 'What should I verify next?']
  return <div className="mx-auto max-w-6xl space-y-8">
    <div className="flex flex-wrap items-end justify-between gap-4"><div><p className="eyebrow">Analyst workspace</p><h1 className="mt-2 text-3xl font-bold tracking-tight text-[var(--ink)]">AI investigation agent</h1><p className="mt-2 max-w-xl text-sm text-[var(--muted)]">Turn raw signals into a focused first-pass triage for your next decision.</p></div><div className="flex items-center gap-2 rounded-full bg-teal-50 px-3 py-2 text-xs font-semibold text-teal-700"><span className="h-2 w-2 rounded-full bg-teal-500" /> Ready to assist</div></div>
    <div className="grid grid-cols-1 gap-6 lg:grid-cols-[1.5fr_0.8fr]">
      <div className="surface rounded-2xl p-6"><div className="mb-6 flex items-center justify-between gap-3"><div className="flex items-center gap-3"><span className="flex h-11 w-11 items-center justify-center rounded-xl bg-[var(--ink)] text-white"><Bot size={22} /></span><div><h2 className="font-semibold text-[var(--ink)]">Ask a case question</h2><p className="text-xs text-[var(--muted)]">Your context stays in this workspace.</p></div></div><button onClick={createConversation} className="btn-primary"><MessageSquarePlus size={15} /> New</button></div><form onSubmit={askAssistant} className="space-y-4"><textarea required value={message} onChange={(event) => setMessage(event.target.value)} placeholder="Describe the signal, user, device or investigation..." rows={6} className="w-full resize-none rounded-xl border border-[var(--line)] bg-slate-50 px-4 py-3 text-sm outline-none focus:border-[var(--cyan)]" /><div className="flex justify-end"><button disabled={loading} type="submit" className="inline-flex items-center gap-2 rounded-lg bg-[var(--ink)] px-4 py-2.5 text-sm font-semibold text-white hover:bg-[var(--cyan)] hover:text-[var(--ink)] disabled:opacity-50"><Send size={16} />{loading ? 'Analyzing...' : 'Run triage'}</button></div></form>{error && <p className="mt-4 rounded-lg bg-red-50 p-3 text-sm text-red-700">{error}</p>}{answer && <div className="mt-6 rounded-xl border border-teal-100 bg-teal-50/60 p-5 text-sm leading-6 text-[var(--ink-soft)]"><div className="mb-3 flex items-center gap-2 font-semibold text-teal-800"><Sparkles size={16} /> Triage output</div><MarkdownMessage content={answer} /></div>}</div>
      <aside className="space-y-6"><div className="surface rounded-2xl p-5"><div className="mb-4 flex items-center justify-between gap-2"><div className="flex items-center gap-2"><Clock3 size={17} className="text-[var(--violet)]" /><h2 className="font-semibold text-[var(--ink)]">Conversations</h2></div><button onClick={() => { setShowArchived(!showArchived); loadConversations(!showArchived) }} className="text-xs font-semibold text-[var(--cyan)]">{showArchived ? 'Active' : 'Archived'}</button></div><div className="mb-4 flex gap-2"><input value={search} onChange={(event) => setSearch(event.target.value)} onKeyDown={(event) => { if (event.key === 'Enter') loadConversations(showArchived, search) }} placeholder="Search conversations..." className="field-control min-w-0 flex-1 py-2 text-xs" /><button onClick={() => loadConversations(showArchived, search)} aria-label="Search conversations" className="btn-primary px-3"><Search size={15} /></button></div><div className="space-y-2">{conversations.length === 0 ? <p className="text-sm text-[var(--muted)]">No conversations found.</p> : conversations.map((conversation) => <div key={conversation.id} className={`flex items-center gap-2 rounded-lg border p-2 ${conversation.id === conversationId ? 'border-[var(--cyan)] bg-teal-50' : 'border-[var(--line)]'}`}><button onClick={() => openConversation(conversation.id)} className="min-w-0 flex-1 truncate text-left text-sm text-[var(--ink-soft)]">{conversation.title}</button><button title={conversation.is_archived ? 'Restore conversation' : 'Archive conversation'} onClick={() => archiveConversation(conversation)} className="text-[var(--muted)] hover:text-[var(--cyan)]"><Archive size={14} /></button><button title="Delete conversation" onClick={() => deleteConversation(conversation)} className="text-[var(--muted)] hover:text-red-600"><Trash2 size={14} /></button></div>)}</div></div><div className="surface rounded-2xl p-5"><div className="mb-4 flex items-center gap-2"><ShieldAlert size={17} className="text-[var(--coral)]" /><h2 className="font-semibold text-[var(--ink)]">Suggested prompts</h2></div><div className="space-y-2">{prompts.map((prompt) => <button key={prompt} onClick={() => setMessage(prompt)} className="w-full rounded-lg border border-[var(--line)] p-3 text-left text-sm text-[var(--ink-soft)] hover:border-[var(--cyan)] hover:bg-teal-50">{prompt}</button>)}</div></div></aside>
    </div>
  </div>
}
