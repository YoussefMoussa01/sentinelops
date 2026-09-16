import { Link, useNavigate } from 'react-router-dom'
import { useEffect, useState } from 'react'
import { ArrowUpRight, Lock, Radar, ShieldCheck } from 'lucide-react'
import { BrandLogo } from '@/components'
import { useAuth } from '@/features/auth'

export const LoginPage = () => {
  const navigate = useNavigate()
  const { login, isLoading, error, isAuthenticated } = useAuth()
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')

  useEffect(() => {
    if (isAuthenticated) navigate('/dashboard')
  }, [isAuthenticated, navigate])

  const handleSubmit = (event: React.FormEvent) => {
    event.preventDefault()
    if (username && password) login({ username, password })
  }

  return (
    <div className="relative flex min-h-screen items-center justify-center overflow-x-hidden bg-[var(--ink)] px-3 py-6 text-white sm:px-6 sm:py-10">
      <div className="pointer-events-none absolute inset-0 opacity-30" style={{ backgroundImage: 'linear-gradient(rgba(255,255,255,.06) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,.06) 1px, transparent 1px)', backgroundSize: '48px 48px' }} />
      <div className="relative grid w-full max-w-5xl overflow-hidden rounded-2xl border border-white/10 bg-white shadow-2xl lg:grid-cols-[1.05fr_0.95fr]">
        <div className="hidden bg-[var(--ink-soft)] p-8 lg:block lg:p-10">
          <BrandLogo />
          <p className="eyebrow mt-16">Threat response console</p>
          <h2 className="mt-4 max-w-md text-4xl font-bold leading-tight text-white">See the signal.<br />Move with confidence.</h2>
          <p className="mt-5 max-w-sm text-sm leading-6 text-white/60">A focused workspace for triaging alerts, investigating risk and coordinating response.</p>
          <div className="mt-10 space-y-4 text-sm text-white/70">
            <div className="flex items-center gap-3"><Radar size={18} className="text-[var(--cyan)]" /> Live security posture</div>
            <div className="flex items-center gap-3"><ShieldCheck size={18} className="text-[var(--cyan)]" /> Role-aware access controls</div>
          </div>
        </div>
        <div className="min-w-0 p-6 text-[var(--ink)] sm:p-10 lg:p-12">
          <div className="mb-8 lg:hidden"><BrandLogo /></div>
          <div className="mb-8">
            <p className="eyebrow">Secure sign in</p>
            <h1 className="mt-2 text-3xl font-bold sm:text-4xl">Welcome back</h1>
            <p className="mt-2 text-sm text-[var(--muted)]">Resume your security operations workspace.</p>
          </div>
          <form onSubmit={handleSubmit} className="space-y-4">
            {error && <div className="rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">{error}</div>}
            <label className="block text-sm font-semibold text-[var(--ink-soft)]">Username<input type="text" value={username} onChange={(event) => setUsername(event.target.value)} className="field-control mt-2" placeholder="Enter your username" disabled={isLoading} /></label>
            <label className="block text-sm font-semibold text-[var(--ink-soft)]">Password<input type="password" value={password} onChange={(event) => setPassword(event.target.value)} className="field-control mt-2" placeholder="Enter your password" disabled={isLoading} /></label>
            <button type="submit" disabled={isLoading || !username || !password} className="btn-primary w-full justify-center py-3 disabled:opacity-50">{isLoading ? 'Signing in...' : 'Sign in'} <ArrowUpRight size={17} /></button>
          </form>
          <div className="mt-8 border-t border-[var(--line)] pt-6">
            <p className="text-center text-xs leading-5 text-[var(--muted)]"><Lock size={13} className="mr-1 inline" /> Access is protected by SentinelOps RBAC.</p>
            <p className="mt-4 text-center text-sm text-[var(--muted)]">Need an account? <Link to="/register" className="font-medium text-[var(--cyan)] hover:underline">Create one</Link></p>
          </div>
        </div>
      </div>
    </div>
  )
}
