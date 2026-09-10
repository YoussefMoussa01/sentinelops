import { useEffect, useRef, useState } from 'react'
import { Bot, ChevronDown, RotateCcw, Send, X } from 'lucide-react'
import { aiAPI } from '@/services/api'
import { MarkdownMessage } from './MarkdownMessage'

interface Message {
  role: 'assistant' | 'user'
  text: string
  reasoningDetails?: unknown
}

export const ChatWidget = () => {
  const [open, setOpen] = useState(false)
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [messages, setMessages] = useState<Message[]>([
    { role: 'assistant', text: 'I can help with SentinelOps alerts, investigations, devices, logs and security operations.' },
  ])
  const messagesEndRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (open) messagesEndRef.current?.scrollIntoView({ behavior: 'smooth', block: 'end' })
  }, [messages, loading, open])

  const resetConversation = () => {
    setMessages([{ role: 'assistant', text: 'I can help with SentinelOps alerts, investigations, devices, logs and security operations.' }])
    setInput('')
  }

  const sendMessage = async (event: React.FormEvent) => {
    event.preventDefault()
    const text = input.trim()
    if (!text || loading) return
    setMessages((current) => [...current, { role: 'user', text }])
    setInput('')
    setLoading(true)
    try {
      const history = messages.slice(1).map((item) => ({
        role: item.role,
        content: item.text,
        ...(item.reasoningDetails !== undefined ? { reasoning_details: item.reasoningDetails } : {}),
      }))
      // The widget is a platform-wide assistant; it must not depend on the active route.
      const response = await aiAPI.queryAssistant(text, undefined, history) as { answer: string; reasoning_details?: unknown }
      setMessages((current) => [...current, { role: 'assistant', text: response.answer, reasoningDetails: response.reasoning_details }])
    } catch (error) {
      setMessages((current) => [...current, { role: 'assistant', text: error instanceof Error ? error.message : 'Assistant unavailable.' }])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="fixed bottom-5 right-5 z-40">
      {open && (
        <div className="mb-3 flex h-[min(34rem,calc(100vh-7rem))] w-[min(25rem,calc(100vw-2rem))] flex-col overflow-hidden rounded-2xl border border-[var(--line)] bg-white shadow-2xl shadow-slate-900/20">
          <div className="flex items-center justify-between bg-[var(--ink)] px-4 py-3 text-white">
            <div className="flex items-center gap-3"><span className="flex h-8 w-8 items-center justify-center rounded-lg bg-[var(--cyan)] text-[var(--ink)]"><Bot size={17} /></span><span><span className="block text-sm font-semibold">SentinelOps assistant</span><span className="font-mono text-[9px] uppercase tracking-wider text-white/50">Platform copilot</span></span></div>
            <div className="flex items-center gap-3"><button aria-label="Clear conversation" title="Clear conversation" onClick={resetConversation} className="text-white/55 transition hover:text-white"><RotateCcw size={15} /></button><button aria-label="Close assistant" onClick={() => setOpen(false)} className="text-white/60 transition hover:text-white"><X size={18} /></button></div>
          </div>
          <div role="log" aria-live="polite" className="chat-messages flex-1 space-y-3 overflow-y-auto bg-slate-50 p-4">
            {messages.map((message, index) => <div key={`${message.role}-${index}`} className={`chat-message max-w-[92%] rounded-xl px-3 py-2 text-sm leading-6 ${message.role === 'user' ? 'ml-auto whitespace-pre-line bg-[var(--ink)] text-white' : 'border border-[var(--line)] bg-white text-[var(--ink-soft)]'}`}>{message.role === 'assistant' ? <MarkdownMessage content={message.text} /> : message.text}</div>)}
            {loading && <div className="flex w-fit items-center gap-2 rounded-xl border border-[var(--line)] bg-white px-3 py-2 text-xs text-[var(--muted)]"><span className="typing-dot" /><span className="typing-dot" /><span className="typing-dot" />Analyzing</div>}
            <div ref={messagesEndRef} aria-hidden="true" />
          </div>
          <form onSubmit={sendMessage} className="flex gap-2 border-t border-[var(--line)] bg-white p-3"><input aria-label="Ask the SentinelOps assistant" value={input} onChange={(event) => setInput(event.target.value)} placeholder="Ask about SentinelOps..." autoComplete="off" className="field-control min-w-0 flex-1 bg-slate-50 py-2" /><button aria-label="Send message" disabled={!input.trim() || loading} className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-[var(--cyan)] text-[var(--ink)] transition hover:bg-[var(--ink)] hover:text-white disabled:cursor-not-allowed disabled:opacity-40"><Send size={16} /></button></form>
        </div>
      )}
      <button aria-label={open ? 'Close assistant' : 'Open assistant'} onClick={() => setOpen(!open)} className="flex h-14 w-14 items-center justify-center rounded-full bg-[var(--ink)] text-white shadow-xl shadow-slate-900/20 transition hover:-translate-y-1 hover:bg-[var(--cyan)] hover:text-[var(--ink)]">{open ? <ChevronDown size={22} /> : <Bot size={22} />}</button>
    </div>
  )
}
