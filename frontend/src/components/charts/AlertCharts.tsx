import {
  Bar, BarChart, CartesianGrid, Cell, Line, LineChart, Pie, PieChart,
  ResponsiveContainer, Tooltip, XAxis, YAxis,
} from 'recharts'

const SEVERITY_COLORS: Record<string, string> = {
  CRITICAL: '#ef4444',
  HIGH: '#f59e0b',
  MEDIUM: '#14b8a6',
  LOW: '#64748b',
}

const STATUS_COLORS: Record<string, string> = {
  NEW: '#0ea5e9',
  ACKNOWLEDGED: '#14b8a6',
  INVESTIGATING: '#8b5cf6',
  RESOLVED: '#22c55e',
  FALSE_POSITIVE: '#94a3b8',
}

interface DistributionRecord { name: string; value: number }
interface TrendRecord { date: string; count: number }

const toDistribution = (distribution: Record<string, number> | undefined): DistributionRecord[] =>
  Object.entries(distribution ?? {}).map(([name, value]) => ({ name, value: Number(value) || 0 }))

const tooltipStyle = {
  borderRadius: 12,
  border: '1px solid var(--line)',
  fontSize: 13,
  background: '#ffffff',
}

export const SeverityPieChart = ({ distribution }: { distribution?: Record<string, number> }) => {
  const data = toDistribution(distribution)
  if (data.length === 0) {
    return (
      <div className="flex h-56 items-center justify-center rounded-xl border border-dashed border-[var(--line)] text-sm text-[var(--muted)]">
        No alert severity data yet.
      </div>
    )
  }
  return (
    <div className="flex h-56 flex-col items-center">
      <ResponsiveContainer width="100%" height="100%">
        <PieChart>
          <Pie data={data} dataKey="value" nameKey="name" innerRadius={45} outerRadius={80} paddingAngle={2}>
            {data.map((entry) => <Cell key={entry.name} fill={SEVERITY_COLORS[entry.name] ?? '#94a3b8'} />)}
          </Pie>
          <Tooltip contentStyle={tooltipStyle} />
        </PieChart>
      </ResponsiveContainer>
      <div className="flex flex-wrap justify-center gap-3 pb-1">
        {data.map((entry) => (
          <span key={entry.name} className="flex items-center gap-1.5 text-xs text-[var(--muted)]">
            <span className="h-2.5 w-2.5 rounded-full" style={{ background: SEVERITY_COLORS[entry.name] ?? '#94a3b8' }} />
            {entry.name} <span className="font-semibold text-[var(--ink)]">{entry.value}</span>
          </span>
        ))}
      </div>
    </div>
  )
}

export const StatusBarChart = ({ distribution }: { distribution?: Record<string, number> }) => {
  const data = toDistribution(distribution)
  if (data.length === 0) {
    return (
      <div className="flex h-56 items-center justify-center rounded-xl border border-dashed border-[var(--line)] text-sm text-[var(--muted)]">
        No alert status data yet.
      </div>
    )
  }
  return (
    <ResponsiveContainer width="100%" height={224}>
      <BarChart data={data} margin={{ top: 8, right: 8, left: -18, bottom: 0 }}>
        <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="var(--line)" />
        <XAxis dataKey="name" tick={{ fontSize: 12, fill: 'var(--muted)' }} axisLine={false} tickLine={false} />
        <YAxis allowDecimals={false} tick={{ fontSize: 12, fill: 'var(--muted)' }} axisLine={false} tickLine={false} />
        <Tooltip cursor={{ fill: 'rgba(20,184,166,0.08)' }} contentStyle={tooltipStyle} />
        <Bar dataKey="value" name="Alerts" radius={[6, 6, 0, 0]}>
          {data.map((entry) => <Cell key={entry.name} fill={STATUS_COLORS[entry.name] ?? '#0ea5e9'} />)}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  )
}

export const AlertTrendChart = ({ trend }: { trend?: TrendRecord[] }) => {
  const data = (trend ?? []).map((item) => ({ ...item, label: item.date.slice(5) }))
  if (data.length === 0) {
    return (
      <div className="flex h-56 items-center justify-center rounded-xl border border-dashed border-[var(--line)] text-sm text-[var(--muted)]">
        No alert activity in the last 7 days.
      </div>
    )
  }
  return (
    <ResponsiveContainer width="100%" height={224}>
      <LineChart data={data} margin={{ top: 8, right: 8, left: -18, bottom: 0 }}>
        <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="var(--line)" />
        <XAxis dataKey="label" tick={{ fontSize: 12, fill: 'var(--muted)' }} axisLine={false} tickLine={false} />
        <YAxis allowDecimals={false} tick={{ fontSize: 12, fill: 'var(--muted)' }} axisLine={false} tickLine={false} />
        <Tooltip contentStyle={tooltipStyle} formatter={(value) => [value, 'Alerts']} labelFormatter={(label) => `Date ${label}`} />
        <Line type="monotone" dataKey="count" name="Alerts" stroke="var(--cyan)" strokeWidth={2.5} dot={{ r: 3, fill: 'var(--cyan)' }} activeDot={{ r: 5 }} />
      </LineChart>
    </ResponsiveContainer>
  )
}