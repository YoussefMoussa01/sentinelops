import { Header } from './Header'
import { Sidebar } from './Sidebar'
import { useAuth } from '@/features/auth'
import { ChatWidget } from './ChatWidget'

interface LayoutProps {
  children: React.ReactNode
}

export const Layout = ({ children }: LayoutProps) => {
  const { isAuthenticated } = useAuth()

  if (!isAuthenticated) {
    return <>{children}</>
  }

  return (
    <div className="app-shell flex h-screen">
      <Sidebar />
      <div className="flex-1 flex flex-col">
        <Header />
        <main className="flex-1 overflow-auto p-4 md:p-7">{children}</main>
      </div>
      <ChatWidget />
    </div>
  )
}
