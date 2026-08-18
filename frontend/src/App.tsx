import { useEffect } from 'react'
import { Router } from '@/app/router/routes'
import { useAppDispatch } from '@/app/store/hooks'
import { restoreSessionRequest } from '@/features/auth'
import './App.css'

function App() {
  const dispatch = useAppDispatch()

  useEffect(() => {
    // Restore session on app load
    dispatch(restoreSessionRequest())
  }, [dispatch])

  return <Router />
}

export default App
