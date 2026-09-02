import { Link, useLocation } from 'react-router-dom'
import {
  AlertCircle,
  FileText,
  Users,
  Server,
  LogOut,
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
  const [expandedItems, setExpandedItems] = useState<string[]>([])

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
      requiredPermission: 'view_alerts',
    },
    {
      label: 'Investigations',
      to: '/investigations',
      icon: <FileText size={20} />,
      requiredPermission: 'view_investigations',
    },
    {
      label: 'Security Data',
      to: '#',
      icon: <Server size={20} />,
      requiredPermission: 'view_users',
      subItems: [
        { label: 'Users', to: '/users', icon: <Users size={18} /> },
        { label: 'Devices', to: '/devices', icon: <Server size={18} /> },
      ],
    },
    {
      label: 'Logs',
      to: '/logs',
      icon: <LogOut size={20} />,
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
    <aside className="w-64 bg-gray-900 text-white h-screen flex flex-col border-r border-gray-700">
      <nav className="flex-1 px-4 py-6 space-y-2 overflow-y-auto">
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
                      ? 'bg-brand-600 text-white'
                      : 'text-gray-300 hover:bg-gray-800'
                  }`}
                >
                  {item.icon}
                  <span className="flex-1 text-left">{item.label}</span>
                  <ChevronDown
                    size={18}
                    className={`transition-transform ${
                      isExpanded ? 'rotate-180' : ''
                    }`}
                  />
                </button>
              ) : (
                <Link
                  to={item.to}
                  className={`flex items-center gap-3 px-4 py-3 rounded-lg transition ${
                    isActive
                      ? 'bg-brand-600 text-white'
                      : 'text-gray-300 hover:bg-gray-800'
                  }`}
                >
                  {item.icon}
                  <span>{item.label}</span>
                </Link>
              )}

              {item.subItems && isExpanded && (
                <div className="ml-4 space-y-1 mt-1 border-l border-gray-700 pl-3">
                  {item.subItems.map((subItem) => (
                    <Link
                      key={subItem.to}
                      to={subItem.to}
                      className={`flex items-center gap-3 px-4 py-2 rounded-lg text-sm transition ${
                        location.pathname === subItem.to
                          ? 'bg-brand-600 text-white'
                          : 'text-gray-400 hover:bg-gray-800'
                      }`}
                    >
                      {subItem.icon}
                      <span>{subItem.label}</span>
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
