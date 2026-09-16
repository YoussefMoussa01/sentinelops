import { Header } from './Header'
import { Sidebar } from './Sidebar'
import { useAuth } from '@/features/auth'
import { ChatWidget } from './ChatWidget'
import { useEffect, useState } from 'react'
import { useLocation } from 'react-router-dom'

interface LayoutProps {
  children: React.ReactNode
}

export const Layout = ({ children }: LayoutProps) => {
  const { isAuthenticated } = useAuth()
  const location = useLocation()
  const [sidebarOpen, setSidebarOpen] = useState(false)

  useEffect(() => {
    setSidebarOpen(false)
  }, [location.pathname])

  useEffect(() => {
    if (!sidebarOpen) return

    const closeOnEscape = (event: KeyboardEvent) => {
      if (event.key === 'Escape') setSidebarOpen(false)
    }
    document.addEventListener('keydown', closeOnEscape)
    document.body.classList.add('sidebar-is-open')

    return () => {
      document.removeEventListener('keydown', closeOnEscape)
      document.body.classList.remove('sidebar-is-open')
    }
  }, [sidebarOpen])

  if (!isAuthenticated) {
    return <>{children}</>
  }

  return (
    <div className="app-shell flex h-screen overflow-hidden">
      <Sidebar open={sidebarOpen} onClose={() => setSidebarOpen(false)} />
      {sidebarOpen && <button aria-label="Close navigation" onClick={() => setSidebarOpen(false)} className="sidebar-overlay" />}
      <div className="flex min-w-0 flex-1 flex-col">
        <Header menuOpen={sidebarOpen} onMenuOpen={() => setSidebarOpen(true)} />
        <main className="min-w-0 flex-1 overflow-auto p-4 md:p-7">{children}</main>
      </div>
      <ChatWidget />
    </div>
  )
}
