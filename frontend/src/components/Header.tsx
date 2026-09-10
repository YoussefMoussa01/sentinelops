import { useState } from 'react'
import { useLocation } from 'react-router-dom'
import { Bell, ChevronDown, LogOut, Search } from 'lucide-react'
import { useAuth } from '@/features/auth'

export const Header = () => {
  const { user, logout } = useAuth()
  const location = useLocation()
  const [showUserMenu, setShowUserMenu] = useState(false)
  const pageName = location.pathname === '/dashboard'
    ? 'Command overview'
    : location.pathname.split('/').filter(Boolean).map((part) => part.replace(/-/g, ' ')).join(' / ')

  return (
    <header className="sticky top-0 z-30 border-b border-[var(--line)] bg-white/85 text-[var(--ink)] backdrop-blur">
      <div className="flex min-h-[4.75rem] items-center justify-between gap-4 px-4 md:px-7">
        <div className="min-w-0"><p className="eyebrow">Security operations center</p><p className="mt-1 truncate text-sm font-semibold capitalize">{pageName}</p></div>

        <div className="flex items-center gap-4">
          <button aria-label="Search workspace" className="hidden h-9 w-9 items-center justify-center rounded-lg border border-[var(--line)] text-[var(--muted)] transition hover:border-[var(--cyan)] hover:text-[var(--cyan)] sm:flex"><Search size={16} /></button>
          <button aria-label="Notifications" className="relative hidden h-9 w-9 items-center justify-center rounded-lg border border-[var(--line)] text-[var(--muted)] transition hover:border-[var(--cyan)] hover:text-[var(--cyan)] sm:flex"><Bell size={16} /><span className="absolute right-1.5 top-1.5 h-1.5 w-1.5 rounded-full bg-[var(--coral)]" /></button>
          {user && (
            <div className="flex items-center gap-2">
              <span className="hidden min-w-0 max-w-[12rem] text-right sm:block"><span className="block truncate text-sm font-semibold" title={user.username}>{user.username}</span><span className="font-mono text-[10px] uppercase text-[var(--muted)]">{user.roles?.[0] || 'operator'}</span></span>
              <div className="relative">
                <button
                  onClick={() => setShowUserMenu(!showUserMenu)}
                  className="flex items-center gap-2 rounded-full border border-[var(--line)] p-1 pr-2 transition hover:border-[var(--cyan)]"
                >
                  <span className="flex h-8 w-8 items-center justify-center rounded-full bg-[var(--ink)] text-sm font-bold text-white">{user.username.slice(0, 1).toUpperCase()}</span><ChevronDown size={14} className="text-[var(--muted)]" />
                </button>
                {showUserMenu && (
                  <div className="absolute right-0 z-10 mt-2 w-[min(18rem,calc(100vw-2rem))] rounded border border-[var(--line)] bg-white text-[var(--ink)] shadow-xl">
                    <div className="min-w-0 border-b px-4 py-2">
                      <p className="truncate font-semibold" title={user.username}>{user.username}</p>
                      <p className="font-mono text-[10px] uppercase text-gray-500">{user.roles?.join(', ')}</p>
                    </div>
                    <button
                      onClick={logout}
                      className="flex w-full items-center gap-2 px-4 py-3 text-left text-sm hover:bg-gray-100"
                    >
                      <LogOut size={16} />
                      Logout
                    </button>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      </div>
    </header>
  )
}
