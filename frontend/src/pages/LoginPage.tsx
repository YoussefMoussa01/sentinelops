import { Link, useNavigate } from 'react-router-dom'
import { useEffect, useState } from 'react'
import { useAuth } from '@/features/auth'
import { ArrowUpRight, Lock, Radar, ShieldCheck } from 'lucide-react'

export const LoginPage = () => {
  const navigate = useNavigate()
  const { login, isLoading, error, isAuthenticated } = useAuth()
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')

  // Navigate to dashboard when login succeeds
  useEffect(() => {
    if (isAuthenticated) {
      navigate('/dashboard')
    }
  }, [isAuthenticated, navigate])

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (username && password) {
      login({ username, password })
    }
  }

  return (
    <div className="relative flex min-h-screen items-center justify-center overflow-hidden bg-[var(--ink)] px-4 py-10 text-white">
      <div className="pointer-events-none absolute inset-0 opacity-30" style={{ backgroundImage: 'linear-gradient(rgba(255,255,255,.06) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,.06) 1px, transparent 1px)', backgroundSize: '48px 48px' }} />
      <div className="relative grid w-full max-w-5xl overflow-hidden rounded-2xl border border-white/10 bg-white shadow-2xl lg:grid-cols-[1.05fr_0.95fr]">
        <div className="hidden bg-[var(--ink-soft)] p-10 lg:block"><div className="flex items-center gap-3"><span className="flex h-10 w-10 items-center justify-center rounded-lg bg-[var(--cyan)] font-bold text-[var(--ink)]">S</span><span className="text-lg font-bold">SentinelOps</span></div><p className="eyebrow mt-20">Threat response console</p><h2 className="mt-4 max-w-md text-4xl font-bold leading-tight text-white">See the signal.<br />Move with confidence.</h2><p className="mt-5 max-w-sm text-sm leading-6 text-white/60">A focused workspace for triaging alerts, investigating risk and coordinating response.</p><div className="mt-12 space-y-4 text-sm text-white/70"><div className="flex items-center gap-3"><Radar size={18} className="text-[var(--cyan)]" /> Live security posture</div><div className="flex items-center gap-3"><ShieldCheck size={18} className="text-[var(--cyan)]" /> Role-aware access controls</div></div></div>
        <div className="p-8 text-[var(--ink)] sm:p-12">
        <div className="mb-8 lg:hidden"><p className="eyebrow">SentinelOps</p><h1 className="mt-2 text-3xl font-bold">Welcome back</h1></div>
        <div className="mb-8 hidden lg:block"><p className="eyebrow">Secure sign in</p><h1 className="mt-2 text-3xl font-bold">Welcome back</h1><p className="mt-2 text-sm text-[var(--muted)]">Resume your security operations workspace.</p></div>

        <form onSubmit={handleSubmit} className="space-y-4">
          {error && (
              <div className="rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
              {error}
            </div>
          )}

          <div>
            <label className="mb-2 block text-sm font-semibold text-[var(--ink-soft)]">
              Username
            </label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="w-full rounded-lg border border-[var(--line)] bg-slate-50 px-4 py-3 text-sm outline-none focus:border-[var(--cyan)] focus:ring-2 focus:ring-teal-100"
              placeholder="Enter your username"
              disabled={isLoading}
            />
          </div>

          <div>
            <label className="mb-2 block text-sm font-semibold text-[var(--ink-soft)]">
              Password
            </label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full rounded-lg border border-[var(--line)] bg-slate-50 px-4 py-3 text-sm outline-none focus:border-[var(--cyan)] focus:ring-2 focus:ring-teal-100"
              placeholder="Enter your password"
              disabled={isLoading}
            />
          </div>

          <button
            type="submit"
            disabled={isLoading || !username || !password}
            className="flex w-full items-center justify-center gap-2 rounded-lg bg-[var(--ink)] py-3 font-semibold text-white transition hover:bg-[var(--cyan)] hover:text-[var(--ink)] disabled:opacity-50"
          >
            {isLoading ? 'Signing in...' : 'Sign in'} <ArrowUpRight size={17} />
          </button>
        </form>

        <div className="mt-8 border-t border-[var(--line)] pt-6">
          <p className="text-sm text-gray-600 text-center">
            <Lock size={14} className="mr-1 inline" /> Test credentials: admin / AdminPassword123!
          </p>
          <p className="mt-4 text-center text-sm text-gray-600">
            Need an account? <Link to="/register" className="font-medium text-brand-600 hover:underline">Create one</Link>
          </p>
        </div>
        </div>
      </div>
    </div>
  )
}
