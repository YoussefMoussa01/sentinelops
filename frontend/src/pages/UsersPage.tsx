import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { usersAPI } from '@/services/api'

interface User { id: string; username: string; email: string; is_active: boolean; role?: string }

export const UsersPage = () => {
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
    try {
      await usersAPI.createUser({ username, email, password, role })
      setUsername(''); setEmail(''); setPassword(''); setRole('VIEWER'); setShowForm(false); loadUsers()
    } catch (requestError) { setError(requestError instanceof Error ? requestError.message : 'Unable to create user') }
  }

  return <div>
    <div className="mb-6 flex flex-wrap items-center justify-between gap-4"><h1 className="text-3xl font-bold text-gray-900">Users</h1><button onClick={() => setShowForm(!showForm)} className="rounded-lg bg-brand-600 px-4 py-2 font-medium text-white">{showForm ? 'Cancel' : 'New user'}</button></div>
    {showForm && <form onSubmit={createUser} className="mb-6 space-y-4 rounded-lg bg-white p-6 shadow"><input required minLength={3} value={username} onChange={(event) => setUsername(event.target.value)} placeholder="Username" className="w-full rounded border border-gray-300 px-3 py-2" /><input required type="email" value={email} onChange={(event) => setEmail(event.target.value)} placeholder="Email" className="w-full rounded border border-gray-300 px-3 py-2" /><input required minLength={8} type="password" value={password} onChange={(event) => setPassword(event.target.value)} placeholder="Temporary password" className="w-full rounded border border-gray-300 px-3 py-2" /><select value={role} onChange={(event) => setRole(event.target.value)} className="w-full rounded border border-gray-300 px-3 py-2"><option>VIEWER</option><option>INVESTIGATOR</option><option>SECURITY_ANALYST</option><option>SOC_ADMIN</option></select><button type="submit" className="rounded bg-gray-900 px-4 py-2 text-white">Create user</button></form>}
    {loading && <p className="text-gray-600">Loading users...</p>}{error && <p className="mb-4 text-red-600">Unable to load users: {error}</p>}
    {!loading && <div className="overflow-hidden rounded-lg bg-white shadow"><div className="divide-y divide-gray-200">{users.length === 0 ? <p className="p-6 text-gray-600">No users found.</p> : users.map((user) => <Link key={user.id} to={`/users/${user.id}`} className="block p-5 hover:bg-gray-50"><div className="flex justify-between"><h2 className="font-semibold text-gray-900">{user.username}</h2><span className={user.is_active ? 'text-sm text-green-600' : 'text-sm text-gray-500'}>{user.role || 'VIEWER'} · {user.is_active ? 'Active' : 'Inactive'}</span></div><p className="mt-1 text-sm text-gray-600">{user.email}</p></Link>)}</div></div>}
  </div>
}
