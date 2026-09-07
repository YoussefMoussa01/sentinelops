import { useEffect, useState } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'
import { usersAPI } from '@/services/api'

interface User { id: string; username: string; email: string; is_active: boolean; role?: string; created_at?: string; updated_at?: string }

export const UserDetailPage = () => {
  const { userId } = useParams<{ userId: string }>(); const navigate = useNavigate()
  const [user, setUser] = useState<User | null>(null); const [editing, setEditing] = useState(false); const [error, setError] = useState('')
  useEffect(() => { if (userId) usersAPI.getUser(userId).then((response) => { const payload = response as { data?: User }; setUser(payload.data || null) }).catch((requestError: Error) => setError(requestError.message)) }, [userId])
  const save = async (event: React.FormEvent<HTMLFormElement>) => { event.preventDefault(); if (!userId || !user) return; const form = new FormData(event.currentTarget); try { const response = await usersAPI.updateUser(userId, { email: form.get('email'), is_active: form.get('is_active') === 'true', role: form.get('role') }); const payload = response as { data?: User }; setUser(payload.data || user); setEditing(false) } catch (requestError) { setError(requestError instanceof Error ? requestError.message : 'Unable to update user') } }
  const remove = async () => { if (userId && window.confirm('Delete this user?')) { await usersAPI.deleteUser(userId); navigate('/users') } }
  if (error) return <p className="text-red-600">Unable to load user: {error}</p>
  if (!user) return <p className="text-gray-600">Loading user...</p>
  return <div><Link to="/users" className="text-sm text-brand-600 hover:underline">Back to users</Link><h1 className="mb-6 mt-3 text-3xl font-bold text-gray-900">User Details</h1><div className="space-y-5 rounded-lg bg-white p-6 shadow"><div className="flex justify-end gap-3"><button onClick={() => setEditing(!editing)} className="rounded border border-gray-300 px-3 py-2">{editing ? 'Cancel' : 'Edit'}</button><button onClick={remove} className="rounded bg-red-600 px-3 py-2 text-white">Delete</button></div>{editing && <form onSubmit={save} className="space-y-4 border-b pb-5"><input name="email" required type="email" defaultValue={user.email} className="w-full rounded border border-gray-300 px-3 py-2" /><select name="role" defaultValue={user.role || 'VIEWER'} className="w-full rounded border border-gray-300 px-3 py-2"><option>VIEWER</option><option>INVESTIGATOR</option><option>SECURITY_ANALYST</option><option>SOC_ADMIN</option></select><select name="is_active" defaultValue={String(user.is_active)} className="rounded border border-gray-300 px-3 py-2"><option value="true">Active</option><option value="false">Inactive</option></select><button type="submit" className="rounded bg-gray-900 px-4 py-2 text-white">Save changes</button></form>}<h2 className="text-2xl font-semibold text-gray-900">{user.username}</h2><p className="text-gray-600">{user.email}</p><p className="text-gray-600">Role: {user.role || 'VIEWER'}</p><p className="text-gray-600">{user.is_active ? 'Active' : 'Inactive'}</p></div></div>
}
