import { useState } from 'react'
import { aiAPI } from '@/services/api'

export const AiPage = () => {
  const [message, setMessage] = useState('')
  const [answer, setAnswer] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const askAssistant = async (event: React.FormEvent) => {
    event.preventDefault()
    if (!message.trim()) return
    setLoading(true); setError('')
    try {
      const response = await aiAPI.queryAssistant(message)
      setAnswer((response as { answer: string }).answer)
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : 'Unable to contact assistant')
    } finally { setLoading(false) }
  }

  return <div>
    <h1 className="mb-6 text-3xl font-bold text-gray-900">AI Investigation Agent</h1>
    <div className="max-w-3xl rounded-lg bg-white p-6 shadow">
      <p className="mb-4 text-gray-600">Ask for a first-pass triage of an alert or investigation.</p>
      <form onSubmit={askAssistant} className="space-y-4">
        <textarea required value={message} onChange={(event) => setMessage(event.target.value)} placeholder="What should I investigate about this alert?" rows={5} className="w-full rounded border border-gray-300 px-3 py-2" />
        <button disabled={loading} type="submit" className="rounded bg-brand-600 px-4 py-2 font-medium text-white disabled:opacity-50">{loading ? 'Analyzing...' : 'Ask assistant'}</button>
      </form>
      {error && <p className="mt-4 text-red-600">{error}</p>}
      {answer && <div className="mt-6 whitespace-pre-line rounded border border-gray-200 bg-gray-50 p-4 text-gray-800"><h2 className="mb-2 font-semibold text-gray-900">Assistant response</h2>{answer}</div>}
    </div>
  </div>
}
