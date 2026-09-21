import { useEffect, useMemo, useState } from 'react'
import { Globe2, MapPin, Pencil, Plus, Search, ShieldAlert, Trash2, X } from 'lucide-react'
import { ipAddressesAPI } from '@/services/api'
import { useAuth } from '@/features/auth/hooks/useAuth'

interface Location { id: string; country?: string; city?: string; timezone?: string }
interface IPAddress { id: string; address: string; is_private: boolean; country?: string; city?: string; reputation_score: number; locations: Location[] }

export const IPAddressesPage = () => {
  const { user } = useAuth()
  const canManageIPs = user?.permissions?.includes('manage_ip_addresses') ?? false
  const [items, setItems] = useState<IPAddress[]>([])
  const [query, setQuery] = useState('')
  const [showForm, setShowForm] = useState(false)
  const [editingId, setEditingId] = useState<string | null>(null)
  const [locationIpId, setLocationIpId] = useState<string | null>(null)
  const [address, setAddress] = useState('')
  const [country, setCountry] = useState('')
  const [city, setCity] = useState('')
  const [timezone, setTimezone] = useState('')
  const [reputation, setReputation] = useState('50')
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')

  const loadAddresses = () => {
    setLoading(true)
    ipAddressesAPI.getIPAddresses()
      .then((response) => setItems(Array.isArray(response) ? response as IPAddress[] : []))
      .catch((requestError: Error) => setError(requestError.message))
      .finally(() => setLoading(false))
  }

  useEffect(() => { loadAddresses() }, [])

  const filteredItems = useMemo(() => {
    const normalized = query.trim().toLowerCase()
    if (!normalized) return items
    return items.filter((item) => [item.address, item.country, item.city].some((value) => value?.toLowerCase().includes(normalized)))
  }, [items, query])
  const editingItem = items.find((item) => item.id === editingId)

  const createAddress = async (event: React.FormEvent) => {
    event.preventDefault(); setError(''); setSaving(true)
    try {
      await ipAddressesAPI.createIPAddress({ address, country: country || undefined, city: city || undefined, reputation_score: Number(reputation) })
      setAddress(''); setCountry(''); setCity(''); setReputation('50'); setShowForm(false); loadAddresses()
    } catch (requestError) { setError(requestError instanceof Error ? requestError.message : 'Unable to register IP address') }
    finally { setSaving(false) }
  }

  const startEditing = (item: IPAddress) => { setEditingId(item.id); setCountry(item.country || ''); setReputation(String(item.reputation_score)) }

  const updateAddress = async (event: React.FormEvent) => {
    event.preventDefault(); if (!editingId) return
    setError(''); setSaving(true)
    try {
      const response = await ipAddressesAPI.updateIPAddress(editingId, { country: country || undefined, city: city || undefined, reputation_score: Number(reputation) }) as IPAddress
      setItems((current) => current.map((item) => item.id === editingId ? { ...item, ...response } : item))
      setEditingId(null); setCountry(''); setCity('')
    } catch (requestError) { setError(requestError instanceof Error ? requestError.message : 'Unable to update IP address') }
    finally { setSaving(false) }
  }

  const addLocation = async (event: React.FormEvent) => {
    event.preventDefault(); if (!locationIpId) return
    setError(''); setSaving(true)
    try {
      const location = await ipAddressesAPI.addLocation(locationIpId, { country: country || undefined, city: city || undefined, timezone: timezone || undefined }) as Location
      setItems((current) => current.map((item) => item.id === locationIpId ? { ...item, locations: [...item.locations, location] } : item))
      setLocationIpId(null); setCountry(''); setCity(''); setTimezone('')
    } catch (requestError) { setError(requestError instanceof Error ? requestError.message : 'Unable to add observed location') }
    finally { setSaving(false) }
  }

  const deleteAddress = async (item: IPAddress) => {
    if (!window.confirm(`Delete IP address ${item.address}?`)) return
    try { await ipAddressesAPI.deleteIPAddress(item.id); setItems((current) => current.filter((currentItem) => currentItem.id !== item.id)) }
    catch (requestError) { setError(requestError instanceof Error ? requestError.message : 'Unable to delete IP address') }
  }

  return <div className="page-frame space-y-6">
    <div className="flex flex-wrap items-end justify-between gap-4"><div><p className="eyebrow">Network intelligence</p><h1 className="mt-2 text-3xl font-bold tracking-tight text-[var(--ink)]">IP addresses</h1><p className="mt-2 text-sm text-[var(--muted)]">Track reputation, ownership context and observed locations across the SOC.</p></div>{canManageIPs && <button onClick={() => setShowForm(!showForm)} className="btn-primary"><Plus size={17} />{showForm ? 'Cancel' : 'Register IP'}</button>}</div>
    {canManageIPs && showForm && <form onSubmit={createAddress} className="surface grid gap-4 rounded-2xl p-6 md:grid-cols-4 md:items-end"><label className="text-sm font-semibold text-[var(--ink-soft)]">Address<input required value={address} onChange={(event) => setAddress(event.target.value)} placeholder="203.0.113.10" className="field-control mt-2" /></label><label className="text-sm font-semibold text-[var(--ink-soft)]">Country<input value={country} onChange={(event) => setCountry(event.target.value)} placeholder="TN" className="field-control mt-2" /></label><label className="text-sm font-semibold text-[var(--ink-soft)]">City<input value={city} onChange={(event) => setCity(event.target.value)} placeholder="Tunis" className="field-control mt-2" /></label><label className="text-sm font-semibold text-[var(--ink-soft)]">Reputation<input type="number" min="0" max="100" value={reputation} onChange={(event) => setReputation(event.target.value)} className="field-control mt-2" /></label><button disabled={saving} type="submit" className="btn-primary disabled:opacity-50">{saving ? 'Saving...' : 'Save address'}</button></form>}
    {error && <p className="rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-700">Unable to update IP intelligence: {error}</p>}
    <form onSubmit={(event) => event.preventDefault()} className="surface flex gap-3 rounded-2xl p-4"><div className="relative min-w-0 flex-1"><Search size={16} className="absolute left-3 top-3 text-[var(--muted)]" /><input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Search address, country or city" className="field-control pl-9" /></div></form>
    {canManageIPs && editingItem && <form onSubmit={updateAddress} className="surface grid gap-3 rounded-2xl bg-teal-50/40 p-5 md:grid-cols-4 md:items-end"><div><p className="text-xs uppercase tracking-wider text-[var(--muted)]">Editing IP</p><p className="mt-2 font-mono text-sm">{editingItem.address}</p></div><input value={country} onChange={(event) => setCountry(event.target.value)} placeholder="Country" className="field-control" /><input value={city} onChange={(event) => setCity(event.target.value)} placeholder="City" className="field-control" /><div className="flex gap-2"><input type="number" min="0" max="100" value={reputation} onChange={(event) => setReputation(event.target.value)} className="field-control w-24" /><button disabled={saving} type="submit" className="btn-primary">{saving ? 'Saving...' : 'Save'}</button><button type="button" onClick={() => setEditingId(null)} className="btn-danger px-3" aria-label="Cancel editing"><X size={15} /></button></div></form>}
    {loading ? <p className="text-[var(--muted)]">Loading IP intelligence...</p> : <div className="surface overflow-hidden rounded-2xl"><div className="border-b border-[var(--line)] bg-slate-50/70 px-5 py-3 text-xs font-semibold uppercase tracking-wider text-[var(--muted)]">{filteredItems.length} tracked addresses</div><div className="divide-y divide-[var(--line)]">{filteredItems.length === 0 ? <p className="p-6 text-[var(--muted)]">No IP addresses found.</p> : filteredItems.map((item) => <article key={item.id} className="data-row p-5"><div className="flex flex-wrap items-center gap-4"><span className="flex h-10 w-10 items-center justify-center rounded-xl bg-teal-50 text-[var(--cyan)]"><Globe2 size={19} /></span><div className="min-w-0 flex-1"><p className="font-semibold text-[var(--ink)]">{item.address}</p><p className="mt-1 text-sm text-[var(--muted)]">{item.country || 'Unknown country'}{item.city ? ` · ${item.city}` : ''} {item.is_private ? '· Private' : '· Public'}</p></div><div className="flex flex-wrap items-center gap-3"><button type="button" onClick={() => setLocationIpId(locationIpId === item.id ? null : item.id)} className="flex items-center gap-1.5 text-xs font-semibold text-[var(--cyan)]"><MapPin size={14} />{item.locations.length} location{item.locations.length === 1 ? '' : 's'}</button><span className={`status-chip ${item.reputation_score < 30 ? 'status-chip--critical' : item.reputation_score < 60 ? 'status-chip--medium' : 'status-chip--active'}`}><ShieldAlert size={12} className="mr-1" />Score {item.reputation_score}</span>{canManageIPs && <><button type="button" onClick={() => startEditing(item)} className="text-[var(--muted)] hover:text-[var(--cyan)]" aria-label={`Edit ${item.address}`}><Pencil size={15} /></button><button type="button" onClick={() => deleteAddress(item)} className="text-[var(--muted)] hover:text-red-600" aria-label={`Delete ${item.address}`}><Trash2 size={15} /></button></>}</div></div>{locationIpId === item.id && <div className="mt-4 border-t border-[var(--line)] pt-4"><p className="text-xs font-semibold uppercase tracking-wider text-[var(--muted)]">Observed locations</p>{item.locations.length > 0 && <div className="mt-2 space-y-2">{item.locations.map((location) => <p key={location.id} className="text-sm text-[var(--ink-soft)]">{location.city || 'Unknown city'}{location.country ? `, ${location.country}` : ''}{location.timezone ? ` · ${location.timezone}` : ''}</p>)}</div>}{canManageIPs && <form onSubmit={addLocation} className="mt-3 grid gap-2 sm:grid-cols-4"><input value={country} onChange={(event) => setCountry(event.target.value)} placeholder="Country" className="field-control" /><input value={city} onChange={(event) => setCity(event.target.value)} placeholder="City" className="field-control" /><input value={timezone} onChange={(event) => setTimezone(event.target.value)} placeholder="Timezone" className="field-control" /><button disabled={saving} type="submit" className="btn-primary disabled:opacity-50">{saving ? 'Saving...' : 'Add location'}</button></form>}</div>}</article>)}</div></div>}
  </div>
}
