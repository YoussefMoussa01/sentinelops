import { useEffect, useRef } from 'react'
import { Router } from '@/app/router/routes'
import { useAppDispatch } from '@/app/store/hooks'
import { restoreSessionRequest } from '@/features/auth'
import './App.css'

function App() {
  const dispatch = useAppDispatch()
  const restored = useRef(false)

  useEffect(() => {
    // Restore session on app load
    if (restored.current) return
    restored.current = true
    dispatch(restoreSessionRequest())
  }, [dispatch])

  return <Router />
}

export default App
