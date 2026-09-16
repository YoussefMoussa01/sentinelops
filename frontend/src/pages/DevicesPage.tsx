import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { Cpu, Plus, Radio } from 'lucide-react'
import { devicesAPI, ipAddressesAPI } from '@/services/api'
import { useAuth } from '@/features/auth/hooks/useAuth'

interface Device { id: string; hostname: string; ip_address?: string; ip_address_id?: string; user_id?: string; user?: { id: string; username: string } | null; device_type: string; operating_system?: string; status: string }
interface IPAddress { id: string; address: string; country?: string; city?: string; reputation_score: number }
interface Assignee { id: string; username: string }

export const DevicesPage = () => {
  const { user } = useAuth()
  const canManageDevices = user?.permissions?.includes('manage_devices') ?? false
  const [devices, setDevices] = useState<Device[]>([])
  const [assignees, setAssignees] = useState<Assignee[]>([])
  const [showForm, setShowForm] = useState(false)
  const [hostname, setHostname] = useState('')
  const [ipAddressId, setIpAddressId] = useState('')
  const [userId, setUserId] = useState('')
  const [ipAddresses, setIpAddresses] = useState<IPAddress[]>([])
  const [operatingSystem, setOperatingSystem] = useState('Windows')
  const [error, setError] = useState('')

  const loadDevices = () => devicesAPI.getDevices()
    .then((response) => setDevices(Array.isArray(response) ? response as Device[] : []))
    .catch((requestError: Error) => setError(requestError.message))

  useEffect(() => {
    loadDevices()
    ipAddressesAPI.getIPAddresses(0, 100).then((response) => {
      if (Array.isArray(response)) setIpAddresses(response as IPAddress[])
    }).catch(() => setIpAddresses([]))
    if (canManageDevices) {
      devicesAPI.getAssignees().then((response) => {
        if (Array.isArray(response)) setAssignees(response as Assignee[])
      }).catch(() => setAssignees([]))
    }
  }, [canManageDevices])

  const createDevice = async (event: React.FormEvent) => {
    event.preventDefault()
    try {
      if (!ipAddressId) throw new Error('Select a managed IP address')
      await devicesAPI.createDevice({ hostname, ip_address_id: ipAddressId, user_id: userId || null, operating_system: operatingSystem, device_type: 'WORKSTATION', status: 'ACTIVE' })
      setHostname(''); setIpAddressId(''); setUserId(''); setOperatingSystem('Windows'); setShowForm(false); loadDevices()
    } catch (requestError) { setError(requestError instanceof Error ? requestError.message : 'Unable to create device') }
  }

  return <div className="page-frame space-y-6">
    <div className="flex flex-wrap items-end justify-between gap-4"><div><p className="eyebrow">Asset inventory</p><h1 className="mt-2 text-3xl font-bold tracking-tight text-[var(--ink)]">Devices</h1><p className="mt-2 text-sm text-[var(--muted)]">Monitor the endpoints connected to your security workspace.</p></div>{canManageDevices && <button onClick={() => setShowForm(!showForm)} className="btn-primary"><Plus size={17} />{showForm ? 'Cancel' : 'New device'}</button>}</div>
    {canManageDevices && showForm && <form onSubmit={createDevice} className="surface rounded-2xl p-6 space-y-4"><div><p className="eyebrow">Register asset</p><h2 className="mt-1 text-xl font-bold">Add a monitored device</h2></div><input required value={hostname} onChange={(event) => setHostname(event.target.value)} placeholder="Hostname" className="field-control" /><select value={operatingSystem} onChange={(event) => setOperatingSystem(event.target.value)} className="field-control"><option>Windows</option><option>Linux</option><option>macOS</option><option>Android</option><option>iOS</option><option>Other</option></select><select value={userId} onChange={(event) => setUserId(event.target.value)} className="field-control"><option value="">Unassigned user</option>{assignees.map((assignee) => <option key={assignee.id} value={assignee.id}>{assignee.username}</option>)}</select><select required value={ipAddressId} onChange={(event) => setIpAddressId(event.target.value)} className="field-control"><option value="">Select a managed IP address</option>{ipAddresses.map((ip) => <option key={ip.id} value={ip.id}>{ip.address}{ip.country ? ` · ${ip.country}` : ''}{ip.city ? ` · ${ip.city}` : ''}</option>)}</select><p className="-mt-2 text-xs text-[var(--muted)]">IP addresses come from IP intelligence. Add one there first if the list is empty.</p><button type="submit" className="btn-primary">Register device</button></form>}
    {error && <p className="rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-700">Unable to load devices: {error}</p>}
    <div className="surface overflow-hidden rounded-2xl"><div className="border-b border-[var(--line)] bg-slate-50/70 px-5 py-3 text-xs font-semibold uppercase tracking-wider text-[var(--muted)]">{devices.length} monitored assets</div><div className="divide-y divide-[var(--line)]">{devices.length === 0 ? <p className="p-6 text-[var(--muted)]">No devices found.</p> : devices.map((device) => { const assignedUser = device.user?.username || assignees.find((assignee) => assignee.id === device.user_id)?.username || 'Unassigned'; return <Link key={device.id} to={`/devices/${device.id}`} className="data-row flex items-center gap-4 p-5"><span className="flex h-10 w-10 items-center justify-center rounded-xl bg-teal-50 text-[var(--cyan)]"><Cpu size={19} /></span><span className="min-w-0 flex-1"><span className="block font-semibold text-[var(--ink)]">{device.hostname}</span><span className="mt-1 block truncate text-sm text-[var(--muted)]">{device.ip_address || 'No IP'} - {device.device_type} - {assignedUser}</span></span><span className="flex items-center gap-2"><Radio size={14} className={device.status === 'ACTIVE' ? 'text-emerald-500' : 'text-[var(--muted)]'} /><span className={`status-chip status-chip--${device.status.toLowerCase()}`}>{device.status}</span></span></Link> })}</div></div>
  </div>
}
