import { useState } from 'react'
import { Bot, Clock3, Send, ShieldAlert, Sparkles } from 'lucide-react'
import { aiAPI } from '@/services/api'
import { MarkdownMessage } from '@/components/MarkdownMessage'

export const AiPage = () => {
  const [message, setMessage] = useState('')
  const [answer, setAnswer] = useState('')
  const [history, setHistory] = useState<string[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const askAssistant = async (event: React.FormEvent) => {
    event.preventDefault()
    if (!message.trim()) return
    setLoading(true); setError('')
    try {
      const response = await aiAPI.queryAssistant(message, 'Current workspace page: AI investigation agent')
      setAnswer((response as { answer: string }).answer)
      setHistory((current) => [message, ...current].slice(0, 4))
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : 'Unable to contact assistant')
    } finally { setLoading(false) }
  }

  const prompts = ['Triage the highest risk alert', 'Summarize this investigation', 'What should I verify next?']
  return <div className="mx-auto max-w-6xl space-y-8">
    <div className="flex flex-wrap items-end justify-between gap-4"><div><p className="eyebrow">Analyst workspace</p><h1 className="mt-2 text-3xl font-bold tracking-tight text-[var(--ink)]">AI investigation agent</h1><p className="mt-2 max-w-xl text-sm text-[var(--muted)]">Turn raw signals into a focused first-pass triage for your next decision.</p></div><div className="flex items-center gap-2 rounded-full bg-teal-50 px-3 py-2 text-xs font-semibold text-teal-700"><span className="h-2 w-2 rounded-full bg-teal-500" /> Ready to assist</div></div>
    <div className="grid grid-cols-1 gap-6 lg:grid-cols-[1.5fr_0.8fr]">
      <div className="surface rounded-2xl p-6"><div className="mb-6 flex items-center gap-3"><span className="flex h-11 w-11 items-center justify-center rounded-xl bg-[var(--ink)] text-white"><Bot size={22} /></span><div><h2 className="font-semibold text-[var(--ink)]">Ask a case question</h2><p className="text-xs text-[var(--muted)]">Your context stays in this workspace.</p></div></div><form onSubmit={askAssistant} className="space-y-4"><textarea required value={message} onChange={(event) => setMessage(event.target.value)} placeholder="Describe the signal, user, device or investigation..." rows={6} className="w-full resize-none rounded-xl border border-[var(--line)] bg-slate-50 px-4 py-3 text-sm outline-none focus:border-[var(--cyan)]" /><div className="flex justify-end"><button disabled={loading} type="submit" className="inline-flex items-center gap-2 rounded-lg bg-[var(--ink)] px-4 py-2.5 text-sm font-semibold text-white hover:bg-[var(--cyan)] hover:text-[var(--ink)] disabled:opacity-50"><Send size={16} />{loading ? 'Analyzing...' : 'Run triage'}</button></div></form>{error && <p className="mt-4 rounded-lg bg-red-50 p-3 text-sm text-red-700">{error}</p>}{answer && <div className="mt-6 rounded-xl border border-teal-100 bg-teal-50/60 p-5 text-sm leading-6 text-[var(--ink-soft)]"><div className="mb-3 flex items-center gap-2 font-semibold text-teal-800"><Sparkles size={16} /> Triage output</div><MarkdownMessage content={answer} /></div>}</div>
      <aside className="space-y-6"><div className="surface rounded-2xl p-5"><div className="mb-4 flex items-center gap-2"><ShieldAlert size={17} className="text-[var(--coral)]" /><h2 className="font-semibold text-[var(--ink)]">Suggested prompts</h2></div><div className="space-y-2">{prompts.map((prompt) => <button key={prompt} onClick={() => setMessage(prompt)} className="w-full rounded-lg border border-[var(--line)] p-3 text-left text-sm text-[var(--ink-soft)] hover:border-[var(--cyan)] hover:bg-teal-50">{prompt}</button>)}</div></div><div className="surface rounded-2xl p-5"><div className="mb-4 flex items-center gap-2"><Clock3 size={17} className="text-[var(--violet)]" /><h2 className="font-semibold text-[var(--ink)]">Recent questions</h2></div>{history.length === 0 ? <p className="text-sm text-[var(--muted)]">Your recent questions will appear here.</p> : <div className="space-y-2">{history.map((item) => <button key={item} onClick={() => setMessage(item)} className="block w-full truncate text-left text-sm text-[var(--ink-soft)] hover:text-[var(--cyan)]">{item}</button>)}</div>}</div></aside>
    </div>
  </div>
}
