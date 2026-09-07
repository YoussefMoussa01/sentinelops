import { Header } from './Header'
import { Sidebar } from './Sidebar'
import { useAuth } from '@/features/auth'

interface LayoutProps {
  children: React.ReactNode
}

export const Layout = ({ children }: LayoutProps) => {
  const { isAuthenticated } = useAuth()

  if (!isAuthenticated) {
    return <>{children}</>
  }

  return (
    <div className="app-shell flex h-screen bg-gray-50">
      <Sidebar />
      <div className="flex-1 flex flex-col">
        <Header />
        <main className="flex-1 overflow-auto p-6 md:p-8">{children}</main>
      </div>
    </div>
  )
}
