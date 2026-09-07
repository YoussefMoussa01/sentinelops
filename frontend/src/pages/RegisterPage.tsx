import { useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { authAPI } from '@/services/api'
import { loginSuccess } from '@/features/auth/state/authSlice'
import { useAppDispatch } from '@/app/store/hooks'
import type { LoginResponse } from '@/features/auth/types/auth.types'

const TOKEN_KEY = import.meta.env.VITE_TOKEN_STORAGE_KEY || 'sentinelops_token'

export const RegisterPage = () => {
  const navigate = useNavigate()
  const dispatch = useAppDispatch()
  const [username, setUsername] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [saving, setSaving] = useState(false)

  useEffect(() => {
    if (localStorage.getItem(TOKEN_KEY)) navigate('/dashboard')
  }, [navigate])

  const submit = async (event: React.FormEvent) => {
    event.preventDefault()
    setSaving(true)
    setError('')
    try {
      const response = await authAPI.register(username, email, password) as LoginResponse
      localStorage.setItem(TOKEN_KEY, response.access_token)
      if (response.refresh_token) localStorage.setItem('sentinelops_refresh_token', response.refresh_token)
      dispatch(loginSuccess({ user: response.user, token: response.access_token, refreshToken: response.refresh_token }))
      navigate('/dashboard')
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : 'Unable to create account')
    } finally {
      setSaving(false)
    }
  }

  return <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-brand-900 to-brand-600 px-4"><div className="w-full max-w-md rounded-lg bg-white p-8 shadow-xl"><h1 className="mb-2 text-3xl font-bold text-brand-900">Create account</h1><p className="mb-8 text-gray-600">Create a viewer account for SentinelOps.</p><form onSubmit={submit} className="space-y-4">{error && <div className="rounded border border-red-200 bg-red-50 px-4 py-3 text-red-700">{error}</div>}<input required minLength={3} value={username} onChange={(event) => setUsername(event.target.value)} placeholder="Username" className="w-full rounded-lg border border-gray-300 px-4 py-2" disabled={saving} /><input required type="email" value={email} onChange={(event) => setEmail(event.target.value)} placeholder="Email" className="w-full rounded-lg border border-gray-300 px-4 py-2" disabled={saving} /><input required minLength={8} type="password" value={password} onChange={(event) => setPassword(event.target.value)} placeholder="Password (8 characters minimum)" className="w-full rounded-lg border border-gray-300 px-4 py-2" disabled={saving} /><button disabled={saving} type="submit" className="w-full rounded-lg bg-brand-600 py-2 font-medium text-white disabled:opacity-50">{saving ? 'Creating account...' : 'Create account'}</button></form><p className="mt-6 text-center text-sm text-gray-600">Already have an account? <Link to="/login" className="font-medium text-brand-600 hover:underline">Sign in</Link></p></div></div>
}