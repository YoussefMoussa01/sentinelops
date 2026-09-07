import { render, screen } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { Sidebar } from './Sidebar'

const authState = { user: { permissions: [] as string[] } }

vi.mock('@/features/auth', () => ({
  useAuth: () => ({ user: authState.user }),
}))

describe('Sidebar permissions', () => {
  beforeEach(() => {
    authState.user.permissions = []
  })

  it('shows public security sections and hides restricted sections', () => {
    render(<MemoryRouter><Sidebar /></MemoryRouter>)

    expect(screen.getByText('Dashboard')).toBeInTheDocument()
    expect(screen.getByText('Alerts')).toBeInTheDocument()
    expect(screen.getByText('Investigations')).toBeInTheDocument()
    expect(screen.queryByText('Logs')).not.toBeInTheDocument()
    expect(screen.queryByText('AI Agent')).not.toBeInTheDocument()
    expect(screen.queryByText('Admin')).not.toBeInTheDocument()
  })

  it('shows restricted sections for an authorized user', () => {
    authState.user.permissions = ['view_users', 'view_logs', 'use_ai_agent', 'manage_users']
    render(<MemoryRouter><Sidebar /></MemoryRouter>)

    expect(screen.getByText('Logs')).toBeInTheDocument()
    expect(screen.getByText('AI Agent')).toBeInTheDocument()
    expect(screen.getByText('Admin')).toBeInTheDocument()
  })
})