import { useEffect, useState } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'
import { ArrowLeft, Pencil, Save, ShieldCheck, Trash2 } from 'lucide-react'
import { usersAPI } from '@/services/api'

interface User { id: string; username: string; email: string; is_active: boolean; role?: string; created_at?: string; updated_at?: string }

const roleTone = (role: string) => ({ SOC_ADMIN: 'critical', SECURITY_ANALYST: 'investigating', INVESTIGATOR: 'low', VIEWER: 'medium' }[role] || 'medium')

export const UserDetailPage = () => {
  const { userId } = useParams<{ userId: string }>(); const navigate = useNavigate()
  const [user, setUser] = useState<User | null>(null); const [editing, setEditing] = useState(false); const [error, setError] = useState('')
  useEffect(() => { if (userId) usersAPI.getUser(userId).then((response) => { const payload = response as { data?: User }; setUser(payload.data || null) }).catch((requestError: Error) => setError(requestError.message)) }, [userId])
  const save = async (event: React.FormEvent<HTMLFormElement>) => { event.preventDefault(); if (!userId || !user) return; const form = new FormData(event.currentTarget); try { const response = await usersAPI.updateUser(userId, { email: form.get('email'), is_active: form.get('is_active') === 'true', role: form.get('role') }); const payload = response as { data?: User }; setUser(payload.data || user); setEditing(false) } catch (requestError) { setError(requestError instanceof Error ? requestError.message : 'Unable to update user') } }
  const remove = async () => { if (userId && window.confirm('Delete this user?')) { await usersAPI.deleteUser(userId); navigate('/users') } }
  if (error) return <div className="detail-shell rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-700">Unable to load user: {error}</div>
  if (!user) return <div className="detail-shell text-[var(--muted)]">Loading user...</div>
  return <div className="detail-shell space-y-6">
    <Link to="/users" className="inline-flex items-center gap-2 text-sm font-semibold text-[var(--cyan)] hover:text-[var(--ink)]"><ArrowLeft size={15} /> Back to users</Link>
    <div className="page-hero rounded-2xl p-6 text-white md:p-8"><div className="relative z-10 flex flex-wrap items-end justify-between gap-5"><div><p className="eyebrow text-[var(--cyan)]">Identity profile</p><h1 className="mt-2 text-3xl font-bold tracking-tight md:text-4xl">{user.username}</h1><p className="mt-2 text-sm text-white/65">{user.email}</p></div><span className={`status-chip status-chip--${user.is_active ? 'active' : 'medium'}`}>{user.is_active ? 'Active' : 'Inactive'}</span></div></div>
    <div className="detail-panel p-6"><div className="mb-6 flex flex-wrap items-center justify-between gap-3"><div className="flex items-center gap-3"><span className="flex h-11 w-11 items-center justify-center rounded-xl bg-violet-50 text-[var(--violet)]"><ShieldCheck size={20} /></span><div><p className="text-xs uppercase tracking-wider text-[var(--muted)]">Access role</p><span className={`status-chip status-chip--${roleTone(user.role || 'VIEWER')}`}>{user.role || 'VIEWER'}</span></div></div><div className="flex gap-2"><button onClick={() => setEditing(!editing)} className="btn-primary"><Pencil size={15} />{editing ? 'Cancel' : 'Edit'}</button><button onClick={remove} className="btn-danger"><Trash2 size={15} />Delete</button></div></div>
      {editing && <form onSubmit={save} className="mb-6 space-y-4 border-b border-[var(--line)] pb-6"><div className="grid grid-cols-1 gap-4 md:grid-cols-3"><input name="email" required type="email" defaultValue={user.email} className="field-control md:col-span-3" /><select name="role" defaultValue={user.role || 'VIEWER'} className="field-control"><option>VIEWER</option><option>INVESTIGATOR</option><option>SECURITY_ANALYST</option><option>SOC_ADMIN</option></select><select name="is_active" defaultValue={String(user.is_active)} className="field-control"><option value="true">Active</option><option value="false">Inactive</option></select></div><button type="submit" className="btn-primary"><Save size={15} /> Save changes</button></form>}
      <dl className="grid grid-cols-1 gap-5 sm:grid-cols-2"><div><dt className="text-xs uppercase tracking-wider text-[var(--muted)]">Username</dt><dd className="mt-1 font-semibold text-[var(--ink)]">{user.username}</dd></div><div><dt className="text-xs uppercase tracking-wider text-[var(--muted)]">Email</dt><dd className="mt-1 text-[var(--ink-soft)]">{user.email}</dd></div><div><dt className="text-xs uppercase tracking-wider text-[var(--muted)]">Created</dt><dd className="mt-1 text-sm text-[var(--ink-soft)]">{user.created_at || 'Unknown'}</dd></div><div><dt className="text-xs uppercase tracking-wider text-[var(--muted)]">Last updated</dt><dd className="mt-1 text-sm text-[var(--ink-soft)]">{user.updated_at || 'Unknown'}</dd></div></dl>
    </div>
  </div>
}
