import { useEffect, useState } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'
import { ArrowLeft, Cpu, Pencil, Save, Trash2 } from 'lucide-react'
import { devicesAPI } from '@/services/api'

interface Device { id: string; hostname: string; ip_address?: string; device_type: string; operating_system?: string; status: string }

export const DeviceDetailPage = () => {
  const { deviceId } = useParams<{ deviceId: string }>(); const navigate = useNavigate()
  const [device, setDevice] = useState<Device | null>(null); const [editing, setEditing] = useState(false); const [error, setError] = useState('')
  useEffect(() => { if (deviceId) devicesAPI.getDevice(deviceId).then((response) => setDevice(response as Device)).catch((requestError: Error) => setError(requestError.message)) }, [deviceId])
  const save = async (event: React.FormEvent<HTMLFormElement>) => { event.preventDefault(); if (!deviceId || !device) return; const form = new FormData(event.currentTarget); try { const response = await devicesAPI.updateDevice(deviceId, { hostname: form.get('hostname'), ip_address: form.get('ip_address'), status: form.get('status') }); setDevice(response as Device); setEditing(false) } catch (requestError) { setError(requestError instanceof Error ? requestError.message : 'Unable to update device') } }
  const remove = async () => { if (deviceId && window.confirm('Delete this device?')) { await devicesAPI.deleteDevice(deviceId); navigate('/devices') } }
  if (error) return <div className="detail-shell rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-700">Unable to load device: {error}</div>
  if (!device) return <div className="detail-shell text-[var(--muted)]">Loading device...</div>
  return <div className="detail-shell space-y-6">
    <Link to="/devices" className="inline-flex items-center gap-2 text-sm font-semibold text-[var(--cyan)] hover:text-[var(--ink)]"><ArrowLeft size={15} /> Back to devices</Link>
    <div className="page-hero rounded-2xl p-6 text-white md:p-8"><div className="relative z-10 flex flex-wrap items-end justify-between gap-5"><div><p className="eyebrow text-[var(--cyan)]">Asset profile</p><h1 className="mt-2 text-3xl font-bold tracking-tight md:text-4xl">{device.hostname}</h1><p className="mt-2 text-sm text-white/65">{device.ip_address || 'No IP address'} - {device.device_type}</p></div><span className={`status-chip status-chip--${device.status.toLowerCase()}`}>{device.status}</span></div></div>
    <div className="detail-panel p-6"><div className="mb-6 flex flex-wrap items-center justify-between gap-3"><div className="flex items-center gap-3"><span className="flex h-11 w-11 items-center justify-center rounded-xl bg-teal-50 text-[var(--cyan)]"><Cpu size={20} /></span><div><p className="text-xs uppercase tracking-wider text-[var(--muted)]">Monitored endpoint</p><p className="font-semibold text-[var(--ink)]">{device.operating_system || 'Operating system unknown'}</p></div></div><div className="flex gap-2"><button onClick={() => setEditing(!editing)} className="btn-primary"><Pencil size={15} />{editing ? 'Cancel' : 'Edit'}</button><button onClick={remove} className="btn-danger"><Trash2 size={15} />Delete</button></div></div>
      {editing && <form onSubmit={save} className="mb-6 space-y-4 border-b border-[var(--line)] pb-6"><input name="hostname" required defaultValue={device.hostname} className="field-control" /><input name="ip_address" defaultValue={device.ip_address} placeholder="IP address" className="field-control" /><select name="status" defaultValue={device.status} className="field-control"><option>ACTIVE</option><option>INACTIVE</option><option>OFFLINE</option></select><button type="submit" className="btn-primary"><Save size={15} /> Save changes</button></form>}
      <dl className="grid grid-cols-1 gap-5 sm:grid-cols-2"><div><dt className="text-xs uppercase tracking-wider text-[var(--muted)]">Hostname</dt><dd className="mt-1 font-semibold text-[var(--ink)]">{device.hostname}</dd></div><div><dt className="text-xs uppercase tracking-wider text-[var(--muted)]">IP address</dt><dd className="mt-1 font-mono text-sm text-[var(--ink-soft)]">{device.ip_address || 'Unknown'}</dd></div><div><dt className="text-xs uppercase tracking-wider text-[var(--muted)]">Device type</dt><dd className="mt-1 text-[var(--ink-soft)]">{device.device_type}</dd></div><div><dt className="text-xs uppercase tracking-wider text-[var(--muted)]">Operating system</dt><dd className="mt-1 text-[var(--ink-soft)]">{device.operating_system || 'Unknown'}</dd></div></dl>
    </div>
  </div>
}
