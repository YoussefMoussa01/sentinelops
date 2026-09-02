import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
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

  return <div>
    <div className="mb-6 flex flex-wrap items-center justify-between gap-4"><h1 className="text-3xl font-bold text-gray-900">Devices</h1><button onClick={() => setShowForm(!showForm)} className="rounded-lg bg-brand-600 px-4 py-2 font-medium text-white">{showForm ? 'Cancel' : 'New device'}</button></div>
    {showForm && <form onSubmit={createDevice} className="mb-6 space-y-4 rounded-lg bg-white p-6 shadow"><input required value={hostname} onChange={(event) => setHostname(event.target.value)} placeholder="Hostname" className="w-full rounded border border-gray-300 px-3 py-2" /><input value={ipAddress} onChange={(event) => setIpAddress(event.target.value)} placeholder="IP address" className="w-full rounded border border-gray-300 px-3 py-2" /><button type="submit" className="rounded bg-gray-900 px-4 py-2 text-white">Create device</button></form>}
    {error && <p className="mb-4 text-red-600">Unable to load devices: {error}</p>}
    <div className="overflow-hidden rounded-lg bg-white shadow"><div className="divide-y divide-gray-200">{devices.length === 0 ? <p className="p-6 text-gray-600">No devices found.</p> : devices.map((device) => <Link key={device.id} to={`/devices/${device.id}`} className="block p-5 hover:bg-gray-50"><div className="flex justify-between"><h2 className="font-semibold text-gray-900">{device.hostname}</h2><span className="text-sm text-gray-500">{device.status}</span></div><p className="mt-1 text-sm text-gray-600">{device.ip_address || 'No IP'} · {device.device_type}</p></Link>)}</div></div>
  </div>
}
