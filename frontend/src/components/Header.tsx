import { useState } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { Menu, X, LogOut, User } from 'lucide-react'
import { useAuth } from '@/features/auth'

export const Header = () => {
  const { user, logout } = useAuth()
  const [showUserMenu, setShowUserMenu] = useState(false)

  return (
    <header className="bg-brand-900 text-white shadow-lg">
      <div className="px-6 py-4 flex items-center justify-between">
        <Link to="/dashboard" className="text-xl font-bold">
          SentinelOps
        </Link>

        <div className="flex items-center gap-4">
          {user && (
            <div className="flex items-center gap-2">
              <span className="text-sm font-medium">{user.username}</span>
              <div className="relative">
                <button
                  onClick={() => setShowUserMenu(!showUserMenu)}
                  className="p-2 hover:bg-brand-600 rounded"
                >
                  <User size={20} />
                </button>
                {showUserMenu && (
                  <div className="absolute right-0 mt-2 w-48 bg-white text-brand-900 rounded shadow-lg">
                    <div className="px-4 py-2 border-b">
                      <p className="font-semibold">{user.email}</p>
                      <p className="text-xs text-gray-600">{user.roles.join(', ')}</p>
                    </div>
                    <button
                      onClick={logout}
                      className="w-full text-left px-4 py-2 hover:bg-gray-100 flex items-center gap-2"
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
