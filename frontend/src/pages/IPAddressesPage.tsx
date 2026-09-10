import { useEffect, useMemo, useState } from 'react'
import { Globe2, MapPin, Plus, Search, ShieldAlert } from 'lucide-react'
import { ipAddressesAPI } from '@/services/api'

interface Location {
  id: string
  country?: string
  city?: string
  timezone?: string
}

interface IPAddress {
  id: string
  address: string
  is_private: boolean
  country?: string
  city?: string
  reputation_score: number
  locations: Location[]
}

export const IPAddressesPage = () => {
  const [items, setItems] = useState<IPAddress[]>([])
  const [query, setQuery] = useState('')
  const [showForm, setShowForm] = useState(false)
  const [address, setAddress] = useState('')
  const [country, setCountry] = useState('')
  const [reputation, setReputation] = useState('50')
  const [loading, setLoading] = useState(true)
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

  const createAddress = async (event: React.FormEvent) => {
    event.preventDefault()
    setError('')
    try {
      await ipAddressesAPI.createIPAddress({ address, country: country || undefined, reputation_score: Number(reputation) })
      setAddress(''); setCountry(''); setReputation('50'); setShowForm(false); loadAddresses()
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : 'Unable to register IP address')
    }
  }

  return <div className="page-frame space-y-6">
    <div className="flex flex-wrap items-end justify-between gap-4">
      <div><p className="eyebrow">Network intelligence</p><h1 className="mt-2 text-3xl font-bold tracking-tight text-[var(--ink)]">IP addresses</h1><p className="mt-2 text-sm text-[var(--muted)]">Track reputation, ownership context and observed locations across the SOC.</p></div>
      <button onClick={() => setShowForm(!showForm)} className="btn-primary"><Plus size={17} />{showForm ? 'Cancel' : 'Register IP'}</button>
    </div>
    {showForm && <form onSubmit={createAddress} className="surface grid gap-4 rounded-2xl p-6 md:grid-cols-4 md:items-end"><label className="text-sm font-semibold text-[var(--ink-soft)]">Address<input required value={address} onChange={(event) => setAddress(event.target.value)} placeholder="203.0.113.10" className="field-control mt-2" /></label><label className="text-sm font-semibold text-[var(--ink-soft)]">Country<input value={country} onChange={(event) => setCountry(event.target.value)} placeholder="TN" className="field-control mt-2" /></label><label className="text-sm font-semibold text-[var(--ink-soft)]">Reputation<input type="number" min="0" max="100" value={reputation} onChange={(event) => setReputation(event.target.value)} className="field-control mt-2" /></label><button type="submit" className="btn-primary">Save address</button></form>}
    {error && <p className="rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-700">Unable to load IP intelligence: {error}</p>}
    <form onSubmit={(event) => event.preventDefault()} className="surface flex gap-3 rounded-2xl p-4"><div className="relative min-w-0 flex-1"><Search size={16} className="absolute left-3 top-3 text-[var(--muted)]" /><input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Search address, country or city" className="field-control pl-9" /></div></form>
    {loading ? <p className="text-[var(--muted)]">Loading IP intelligence...</p> : <div className="surface overflow-hidden rounded-2xl"><div className="border-b border-[var(--line)] bg-slate-50/70 px-5 py-3 text-xs font-semibold uppercase tracking-wider text-[var(--muted)]">{filteredItems.length} tracked addresses</div><div className="divide-y divide-[var(--line)]">{filteredItems.length === 0 ? <p className="p-6 text-[var(--muted)]">No IP addresses found.</p> : filteredItems.map((item) => <div key={item.id} className="data-row flex flex-wrap items-center gap-4 p-5"><span className="flex h-10 w-10 items-center justify-center rounded-xl bg-teal-50 text-[var(--cyan)]"><Globe2 size={19} /></span><div className="min-w-0 flex-1"><p className="font-semibold text-[var(--ink)]">{item.address}</p><p className="mt-1 text-sm text-[var(--muted)]">{item.country || 'Unknown country'}{item.city ? ` · ${item.city}` : ''} {item.is_private ? '· Private' : '· Public'}</p></div><div className="flex items-center gap-4"><span className="flex items-center gap-1.5 text-xs text-[var(--muted)]"><MapPin size={14} />{item.locations.length} location{item.locations.length === 1 ? '' : 's'}</span><span className={`status-chip ${item.reputation_score < 30 ? 'status-chip--critical' : item.reputation_score < 60 ? 'status-chip--medium' : 'status-chip--active'}`}><ShieldAlert size={12} className="mr-1" />Score {item.reputation_score}</span></div></div>)}</div></div>}
  </div>
}
