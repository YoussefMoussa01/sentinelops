import { useState } from 'react'
import { Bot, ChevronDown, Send, X } from 'lucide-react'
import { aiAPI } from '@/services/api'

interface Message {
  role: 'assistant' | 'user'
  text: string
}

export const ChatWidget = () => {
  const [open, setOpen] = useState(false)
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [messages, setMessages] = useState<Message[]>([
    { role: 'assistant', text: 'Ready to help triage an alert or investigation.' },
  ])

  const sendMessage = async (event: React.FormEvent) => {
    event.preventDefault()
    const text = input.trim()
    if (!text || loading) return
    setMessages((current) => [...current, { role: 'user', text }])
    setInput('')
    setLoading(true)
    try {
      const response = await aiAPI.queryAssistant(text) as { answer: string }
      setMessages((current) => [...current, { role: 'assistant', text: response.answer }])
    } catch (error) {
      setMessages((current) => [...current, { role: 'assistant', text: error instanceof Error ? error.message : 'Assistant unavailable.' }])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="fixed bottom-5 right-5 z-40">
      {open && (
        <div className="mb-3 flex h-[min(30rem,calc(100vh-7rem))] w-[min(22rem,calc(100vw-2rem))] flex-col overflow-hidden rounded-2xl border border-[var(--line)] bg-white shadow-2xl shadow-slate-900/20">
          <div className="flex items-center justify-between bg-[var(--ink)] px-4 py-3 text-white">
            <div className="flex items-center gap-3"><span className="flex h-8 w-8 items-center justify-center rounded-lg bg-[var(--cyan)] text-[var(--ink)]"><Bot size={17} /></span><span><span className="block text-sm font-semibold">Triage copilot</span><span className="font-mono text-[9px] uppercase tracking-wider text-white/50">Online assistant</span></span></div>
            <button aria-label="Close assistant" onClick={() => setOpen(false)} className="text-white/60 hover:text-white"><X size={18} /></button>
          </div>
          <div className="flex-1 space-y-3 overflow-y-auto bg-slate-50 p-4">
            {messages.map((message, index) => <div key={`${message.role}-${index}`} className={`max-w-[88%] whitespace-pre-line rounded-xl px-3 py-2 text-sm ${message.role === 'user' ? 'ml-auto bg-[var(--ink)] text-white' : 'border border-[var(--line)] bg-white text-[var(--ink-soft)]'}`}>{message.text}</div>)}
            {loading && <div className="text-xs text-[var(--muted)]">Analyzing...</div>}
          </div>
          <form onSubmit={sendMessage} className="flex gap-2 border-t border-[var(--line)] bg-white p-3"><input aria-label="Ask the assistant" value={input} onChange={(event) => setInput(event.target.value)} placeholder="Ask about a case..." className="min-w-0 flex-1 rounded-lg border border-[var(--line)] px-3 py-2 text-sm outline-none focus:border-[var(--cyan)]" /><button aria-label="Send message" disabled={!input.trim() || loading} className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-[var(--cyan)] text-[var(--ink)] disabled:opacity-40"><Send size={16} /></button></form>
        </div>
      )}
      <button aria-label={open ? 'Close assistant' : 'Open assistant'} onClick={() => setOpen(!open)} className="flex h-14 w-14 items-center justify-center rounded-full bg-[var(--ink)] text-white shadow-xl shadow-slate-900/20 transition hover:-translate-y-1 hover:bg-[var(--cyan)] hover:text-[var(--ink)]">{open ? <ChevronDown size={22} /> : <Bot size={22} />}</button>
    </div>
  )
}
