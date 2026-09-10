import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { KeyRound, Plus, ShieldCheck, User } from 'lucide-react'
import { usersAPI } from '@/services/api'
import { useAuth } from '@/features/auth'

interface User { id: string; username: string; email: string; is_active: boolean; role?: string }

const roleTone = (role: string) => ({
  SOC_ADMIN: 'critical',
  SUPER_ADMIN: 'critical',
  SECURITY_ANALYST: 'investigating',
  INVESTIGATOR: 'low',
  VIEWER: 'medium',
}[role] || 'medium')

export const UsersPage = () => {
  const { user: currentUser } = useAuth()
  const canCreateSuperAdmin = currentUser?.roles?.includes('SUPER_ADMIN')
  const [users, setUsers] = useState<User[]>([])
  const [showForm, setShowForm] = useState(false)
  const [username, setUsername] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [role, setRole] = useState('VIEWER')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const loadUsers = () => {
    setLoading(true)
    usersAPI.getUsers().then((response) => {
      const payload = response as { data?: User[] }
      setUsers(payload.data || [])
    }).catch((requestError: Error) => setError(requestError.message)).finally(() => setLoading(false))
  }

  useEffect(() => { loadUsers() }, [])

  const createUser = async (event: React.FormEvent) => {
    event.preventDefault()
    setError('')
    try {
      await usersAPI.createUser({ username, email, password, role })
      setUsername(''); setEmail(''); setPassword(''); setRole('VIEWER'); setShowForm(false); loadUsers()
    } catch (requestError) { setError(requestError instanceof Error ? requestError.message : 'Unable to create user') }
  }

  return <div className="page-frame space-y-6">
    <div className="flex flex-wrap items-end justify-between gap-4"><div><p className="eyebrow">Identity control</p><h1 className="mt-2 text-3xl font-bold tracking-tight text-[var(--ink)]">Users</h1><p className="mt-2 text-sm text-[var(--muted)]">Manage analyst identities, roles and access to the operations workspace.</p></div><button onClick={() => setShowForm(!showForm)} className="btn-primary"><Plus size={17} />{showForm ? 'Cancel' : 'New user'}</button></div>
    <div className="grid grid-cols-1 gap-4 sm:grid-cols-3"><div className="surface rounded-2xl p-4"><p className="text-xs uppercase tracking-wider text-[var(--muted)]">Total identities</p><p className="mt-2 text-2xl font-bold text-[var(--ink)]">{users.length}</p></div><div className="surface rounded-2xl p-4"><p className="text-xs uppercase tracking-wider text-[var(--muted)]">Active</p><p className="mt-2 text-2xl font-bold text-emerald-600">{users.filter((user) => user.is_active).length}</p></div><div className="surface rounded-2xl p-4"><p className="text-xs uppercase tracking-wider text-[var(--muted)]">Protected admins</p><p className="mt-2 text-2xl font-bold text-[var(--violet)]">{users.filter((user) => user.role === 'SOC_ADMIN' || user.role === 'SUPER_ADMIN').length}</p></div></div>
    {showForm && <form onSubmit={createUser} className="surface rounded-2xl p-6 space-y-4"><div><p className="eyebrow">Provision identity</p><h2 className="mt-1 text-xl font-bold">Create an operator account</h2><p className="mt-1 text-sm text-[var(--muted)]">Assign the minimum role needed for the user&apos;s work.</p></div><div className="grid grid-cols-1 gap-4 md:grid-cols-2"><input required minLength={3} value={username} onChange={(event) => setUsername(event.target.value)} placeholder="Username" className="field-control" /><input required type="email" value={email} onChange={(event) => setEmail(event.target.value)} placeholder="Email address" className="field-control" /><input required minLength={8} type="password" value={password} onChange={(event) => setPassword(event.target.value)} placeholder="Temporary password" className="field-control" /><select value={role} onChange={(event) => setRole(event.target.value)} className="field-control"><option>VIEWER</option><option>INVESTIGATOR</option><option>SECURITY_ANALYST</option><option>SOC_ADMIN</option>{canCreateSuperAdmin && <option>SUPER_ADMIN</option>}</select></div><button type="submit" className="btn-primary"><KeyRound size={16} /> Create user</button></form>}
    {loading && <p className="text-[var(--muted)]">Loading users...</p>}{error && <p className="rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-700">Unable to load users: {error}</p>}
    {!loading && <div className="surface overflow-hidden rounded-2xl"><div className="border-b border-[var(--line)] bg-slate-50/70 px-5 py-3 text-xs font-semibold uppercase tracking-wider text-[var(--muted)]">{users.length} identities in directory</div><div className="divide-y divide-[var(--line)]">{users.length === 0 ? <p className="p-6 text-[var(--muted)]">No users found.</p> : users.map((user) => <Link key={user.id} to={`/users/${user.id}`} className="data-row flex items-center gap-4 p-5"><span className="flex h-10 w-10 items-center justify-center rounded-xl bg-violet-50 text-[var(--violet)]"><User size={19} /></span><span className="min-w-0 flex-1"><span className="block font-semibold text-[var(--ink)]">{user.username}</span><span className="mt-1 block truncate text-sm text-[var(--muted)]">{user.email}</span></span><span className="hidden items-center gap-2 sm:flex"><ShieldCheck size={14} className="text-[var(--violet)]" /><span className={`status-chip status-chip--${roleTone(user.role || 'VIEWER')}`}>{user.role || 'VIEWER'}</span></span><span className={`status-chip ${user.is_active ? 'status-chip--active' : 'status-chip--medium'}`}>{user.is_active ? 'Active' : 'Inactive'}</span></Link>)}</div></div>}
  </div>
}
