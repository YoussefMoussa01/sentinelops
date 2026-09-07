import { useState } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { LogOut } from 'lucide-react'
import { useAuth } from '@/features/auth'

export const Header = () => {
  const { user, logout } = useAuth()
  const location = useLocation()
  const [showUserMenu, setShowUserMenu] = useState(false)

  return (
    <header className="border-b border-[var(--line)] bg-white/90 text-[var(--ink)] backdrop-blur">
      <div className="flex items-center justify-between px-6 py-4">
        <div><p className="eyebrow">Security operations center</p><p className="mt-1 text-sm font-semibold">{location.pathname === '/dashboard' ? 'Command overview' : location.pathname.replace('/', '').replace(/\//g, ' / ')}</p></div>

        <div className="flex items-center gap-4">
          {user && (
            <div className="flex items-center gap-2">
              <span className="hidden text-right sm:block"><span className="block text-sm font-semibold">{user.username}</span><span className="font-mono text-[10px] uppercase text-[var(--muted)]">{user.roles?.[0] || 'operator'}</span></span>
              <div className="relative">
                <button
                  onClick={() => setShowUserMenu(!showUserMenu)}
                  className="flex h-10 w-10 items-center justify-center rounded-full bg-[var(--ink)] text-sm font-bold text-white hover:bg-[var(--cyan)]"
                >
                  {user.username.slice(0, 1).toUpperCase()}
                </button>
                {showUserMenu && (
                  <div className="absolute right-0 z-10 mt-2 w-56 rounded border border-[var(--line)] bg-white text-[var(--ink)] shadow-xl">
                    <div className="px-4 py-2 border-b">
                      <p className="font-semibold">{user.email}</p>
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
