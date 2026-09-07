import { Link, useLocation } from 'react-router-dom'
import {
  AlertCircle,
  FileText,
  Users,
  Server,
  ScrollText,
  BarChart3,
  Zap,
  Settings,
  ChevronDown,
} from 'lucide-react'
import { useState } from 'react'
import { useAuth } from '@/features/auth'

interface NavItem {
  label: string
  to: string
  icon: React.ReactNode
  requiredPermission?: string
  subItems?: NavItem[]
}

export const Sidebar = () => {
  const location = useLocation()
  const { user } = useAuth()
  const [expandedItems, setExpandedItems] = useState<string[]>(['Security Data'])

  const toggleExpand = (label: string) => {
    setExpandedItems((prev) =>
      prev.includes(label) ? prev.filter((l) => l !== label) : [...prev, label]
    )
  }

  const navItems: NavItem[] = [
    {
      label: 'Dashboard',
      to: '/dashboard',
      icon: <BarChart3 size={20} />,
    },
    {
      label: 'Alerts',
      to: '/alerts',
      icon: <AlertCircle size={20} />,
    },
    {
      label: 'Investigations',
      to: '/investigations',
      icon: <FileText size={20} />,
    },
    {
      label: 'Security Data',
      to: '#',
      icon: <Server size={20} />,
      requiredPermission: 'view_devices',
      subItems: [
        { label: 'Users', to: '/users', icon: <Users size={18} />, requiredPermission: 'view_users' },
        { label: 'Devices', to: '/devices', icon: <Server size={18} />, requiredPermission: 'view_devices' },
      ],
    },
    {
      label: 'Logs',
      to: '/logs',
      icon: <ScrollText size={20} />,
      requiredPermission: 'view_logs',
    },
    {
      label: 'AI Agent',
      to: '/ai',
      icon: <Zap size={20} />,
      requiredPermission: 'use_ai_agent',
    },
    {
      label: 'Admin',
      to: '/admin',
      icon: <Settings size={20} />,
      requiredPermission: 'manage_users',
    },
  ]

  const visibleItems = navItems.filter((item) => {
    if (!item.requiredPermission) return true
    return user?.permissions?.includes(item.requiredPermission)
  })

  return (
    <aside className="flex h-screen w-64 flex-col border-r border-[#243247] bg-[var(--ink)] text-white">
      <div className="border-b border-white/10 px-5 py-6">
        <Link to="/dashboard" className="flex items-center gap-3">
          <span className="flex h-9 w-9 items-center justify-center rounded-lg bg-[var(--cyan)] font-bold text-[var(--ink)]">S</span>
          <span className="brand-copy"><span className="block text-lg font-bold tracking-tight">SentinelOps</span><span className="block text-[10px] uppercase tracking-[0.16em] text-white/45">Threat response</span></span>
        </Link>
      </div>
      <nav className="flex-1 space-y-2 overflow-y-auto px-3 py-6">
        {visibleItems.map((item) => {
          const isActive =
            location.pathname === item.to || location.pathname.startsWith(item.to + '/')
          const isExpanded = expandedItems.includes(item.label)

          return (
            <div key={item.label}>
              {item.subItems ? (
                <button
                  onClick={() => toggleExpand(item.label)}
                  className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition ${
                    isActive
                      ? 'bg-[var(--cyan)] text-[var(--ink)] shadow-lg shadow-teal-950/20'
                      : 'text-gray-300 hover:bg-white/10'
                  }`}
                >
                  {item.icon}
                  <span className="nav-label flex-1 text-left">{item.label}</span>
                  <ChevronDown
                    size={18}
                    className={`nav-chevron transition-transform ${
                      isExpanded ? 'rotate-180' : ''
                    }`}
                  />
                </button>
              ) : (
                <Link
                  to={item.to}
                  className={`flex items-center gap-3 px-4 py-3 rounded-lg transition ${
                    isActive
                    ? 'bg-[var(--cyan)] text-[var(--ink)] shadow-lg shadow-teal-950/20'
                    : 'text-gray-300 hover:bg-white/10'
                  }`}
                >
                  {item.icon}
                  <span className="nav-label">{item.label}</span>
                </Link>
              )}

              {item.subItems && isExpanded && (
                <div className="ml-4 space-y-1 mt-1 border-l border-gray-700 pl-3">
                  {item.subItems.filter((subItem) => !subItem.requiredPermission || user?.permissions?.includes(subItem.requiredPermission)).map((subItem) => (
                    <Link
                      key={subItem.to}
                      to={subItem.to}
                      className={`flex items-center gap-3 px-4 py-2 rounded-lg text-sm transition ${
                        location.pathname === subItem.to
                          ? 'bg-white/10 text-white'
                          : 'text-gray-400 hover:bg-white/10'
                      }`}
                    >
                      {subItem.icon}
                      <span className="nav-label">{subItem.label}</span>
                    </Link>
                  ))}
                </div>
              )}
            </div>
          )
        })}
      </nav>
    </aside>
  )
}
