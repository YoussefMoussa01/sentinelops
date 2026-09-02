import { useEffect, useState } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'
import { devicesAPI } from '@/services/api'

interface Device { id: string; hostname: string; ip_address?: string; device_type: string; operating_system?: string; status: string }

export const DeviceDetailPage = () => {
  const { deviceId } = useParams<{ deviceId: string }>(); const navigate = useNavigate()
  const [device, setDevice] = useState<Device | null>(null); const [editing, setEditing] = useState(false); const [error, setError] = useState('')
  useEffect(() => { if (deviceId) devicesAPI.getDevice(deviceId).then((response) => setDevice(response as Device)).catch((requestError: Error) => setError(requestError.message)) }, [deviceId])
  const save = async (event: React.FormEvent<HTMLFormElement>) => { event.preventDefault(); if (!deviceId || !device) return; const form = new FormData(event.currentTarget); try { const response = await devicesAPI.updateDevice(deviceId, { hostname: form.get('hostname'), ip_address: form.get('ip_address'), status: form.get('status') }); setDevice(response as Device); setEditing(false) } catch (requestError) { setError(requestError instanceof Error ? requestError.message : 'Unable to update device') } }
  const remove = async () => { if (deviceId && window.confirm('Delete this device?')) { await devicesAPI.deleteDevice(deviceId); navigate('/devices') } }
  if (error) return <p className="text-red-600">Unable to load device: {error}</p>
  if (!device) return <p className="text-gray-600">Loading device...</p>
  return <div><Link to="/devices" className="text-sm text-brand-600 hover:underline">Back to devices</Link><h1 className="mb-6 mt-3 text-3xl font-bold text-gray-900">Device Details</h1><div className="space-y-5 rounded-lg bg-white p-6 shadow"><div className="flex justify-end gap-3"><button onClick={() => setEditing(!editing)} className="rounded border border-gray-300 px-3 py-2">{editing ? 'Cancel' : 'Edit'}</button><button onClick={remove} className="rounded bg-red-600 px-3 py-2 text-white">Delete</button></div>{editing && <form onSubmit={save} className="space-y-4 border-b pb-5"><input name="hostname" required defaultValue={device.hostname} className="w-full rounded border border-gray-300 px-3 py-2" /><input name="ip_address" defaultValue={device.ip_address} className="w-full rounded border border-gray-300 px-3 py-2" /><select name="status" defaultValue={device.status} className="rounded border border-gray-300 px-3 py-2"><option>ACTIVE</option><option>INACTIVE</option><option>OFFLINE</option></select><button type="submit" className="rounded bg-gray-900 px-4 py-2 text-white">Save changes</button></form>}<h2 className="text-2xl font-semibold text-gray-900">{device.hostname}</h2><p className="text-gray-600">{device.ip_address || 'No IP address'} · {device.device_type}</p><p className="text-gray-600">{device.operating_system || 'Operating system unknown'} · {device.status}</p></div></div>
}
