import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { Cpu, Plus, Radio } from 'lucide-react'
import { devicesAPI } from '@/services/api'

interface Device { id: string; hostname: string; ip_address?: string; device_type: string; operating_system?: string; status: string }

export const DevicesPage = () => {
  const [devices, setDevices] = useState<Device[]>([])
  const [showForm, setShowForm] = useState(false)
  const [hostname, setHostname] = useState('')
  const [ipAddress, setIpAddress] = useState('')
  const [error, setError] = useState('')

  const loadDevices = () => devicesAPI.getDevices().then((response) => setDevices(Array.isArray(response) ? response as Device[] : [])).catch((requestError: Error) => setError(requestError.message))
  useEffect(() => { loadDevices() }, [])

  const createDevice = async (event: React.FormEvent) => {
    event.preventDefault()
    try {
      await devicesAPI.createDevice({ hostname, ip_address: ipAddress, device_type: 'WORKSTATION', status: 'ACTIVE' })
      setHostname(''); setIpAddress(''); setShowForm(false); loadDevices()
    } catch (requestError) { setError(requestError instanceof Error ? requestError.message : 'Unable to create device') }
  }

  return <div className="page-frame space-y-6">
    <div className="flex flex-wrap items-end justify-between gap-4"><div><p className="eyebrow">Asset inventory</p><h1 className="mt-2 text-3xl font-bold tracking-tight text-[var(--ink)]">Devices</h1><p className="mt-2 text-sm text-[var(--muted)]">Monitor the endpoints connected to your security workspace.</p></div><button onClick={() => setShowForm(!showForm)} className="btn-primary"><Plus size={17} />{showForm ? 'Cancel' : 'New device'}</button></div>
    {showForm && <form onSubmit={createDevice} className="surface rounded-2xl p-6 space-y-4"><div><p className="eyebrow">Register asset</p><h2 className="mt-1 text-xl font-bold">Add a monitored device</h2></div><input required value={hostname} onChange={(event) => setHostname(event.target.value)} placeholder="Hostname" className="field-control" /><input value={ipAddress} onChange={(event) => setIpAddress(event.target.value)} placeholder="IP address" className="field-control" /><button type="submit" className="btn-primary">Register device</button></form>}
    {error && <p className="rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-700">Unable to load devices: {error}</p>}
    <div className="surface overflow-hidden rounded-2xl"><div className="border-b border-[var(--line)] bg-slate-50/70 px-5 py-3 text-xs font-semibold uppercase tracking-wider text-[var(--muted)]">{devices.length} monitored assets</div><div className="divide-y divide-[var(--line)]">{devices.length === 0 ? <p className="p-6 text-[var(--muted)]">No devices found.</p> : devices.map((device) => <Link key={device.id} to={`/devices/${device.id}`} className="data-row flex items-center gap-4 p-5"><span className="flex h-10 w-10 items-center justify-center rounded-xl bg-teal-50 text-[var(--cyan)]"><Cpu size={19} /></span><span className="min-w-0 flex-1"><span className="block font-semibold text-[var(--ink)]">{device.hostname}</span><span className="mt-1 block truncate text-sm text-[var(--muted)]">{device.ip_address || 'No IP'} - {device.device_type}</span></span><span className="flex items-center gap-2"><Radio size={14} className={device.status === 'ACTIVE' ? 'text-emerald-500' : 'text-[var(--muted)]'} /><span className={`status-chip status-chip--${device.status.toLowerCase()}`}>{device.status}</span></span></Link>)}</div></div>
  </div>
}
