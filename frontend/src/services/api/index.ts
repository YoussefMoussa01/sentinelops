import { apiClient } from './client'

// Auth API
export const authAPI = {
  login: async (username: string, password: string) => {
    return apiClient.post('/auth/login', { username, password })
  },
  logout: async () => {
    return apiClient.post('/auth/logout', {})
  },
  getCurrentUser: async () => {
    return apiClient.get('/auth/me')
  },
  refreshToken: async () => {
    return apiClient.post('/auth/refresh', {})
  },
}

// Alerts API
export const alertsAPI = {
  getAlerts: async () => {
    return apiClient.get('/alerts')
  },
  getAlert: async (id: string) => {
    return apiClient.get(`/alerts/${id}`)
  },
  createAlert: async (data: unknown) => {
    return apiClient.post('/alerts', data)
  },
  updateAlert: async (id: string, data: unknown) => {
    return apiClient.patch(`/alerts/${id}`, data)
  },
  deleteAlert: async (id: string) => {
    return apiClient.delete(`/alerts/${id}`)
  },
}

// Investigations API
export const investigationsAPI = {
  getInvestigations: async () => {
    return apiClient.get('/investigations')
  },
  getInvestigation: async (id: string) => {
    return apiClient.get(`/investigations/${id}`)
  },
  createInvestigation: async (data: unknown) => {
    return apiClient.post('/investigations', data)
  },
  updateInvestigation: async (id: string, data: unknown) => {
    return apiClient.patch(`/investigations/${id}`, data)
  },
  deleteInvestigation: async (id: string) => {
    return apiClient.delete(`/investigations/${id}`)
  },
}

// Dashboard API
export const dashboardAPI = {
  getStats: async () => {
    return apiClient.get('/dashboard/stats')
  },
}

// Users API
export const usersAPI = {
  getUsers: async () => {
    return apiClient.get('/admin/users')
  },
  getUser: async (id: string) => {
    return apiClient.get(`/admin/users/${id}`)
  },
  createUser: async (data: unknown) => {
    return apiClient.post('/admin/users', data)
  },
  updateUser: async (id: string, data: unknown) => {
    return apiClient.patch(`/admin/users/${id}`, data)
  },
  deleteUser: async (id: string) => {
    return apiClient.delete(`/admin/users/${id}`)
  },
}

// Devices API
export const devicesAPI = {
  getDevices: async () => {
    return apiClient.get('/devices')
  },
  getDevice: async (id: string) => {
    return apiClient.get(`/devices/${id}`)
  },
  createDevice: async (data: unknown) => {
    return apiClient.post('/devices', data)
  },
  updateDevice: async (id: string, data: unknown) => {
    return apiClient.patch(`/devices/${id}`, data)
  },
  deleteDevice: async (id: string) => {
    return apiClient.delete(`/devices/${id}`)
  },
}

// Logs API
export const logsAPI = {
  getLogs: async () => {
    return apiClient.get('/logs')
  },
  searchLogs: async (query: string) => {
    return apiClient.get('/logs/search', { query })
  },
}

// AI API
export const aiAPI = {
  getConversations: async () => {
    return apiClient.get('/ai/conversations')
  },
  getConversation: async (id: string) => {
    return apiClient.get(`/ai/conversations/${id}`)
  },
  createConversation: async (data: unknown) => {
    return apiClient.post('/ai/conversations', data)
  },
  sendMessage: async (conversationId: string, message: string) => {
    return apiClient.post(`/ai/conversations/${conversationId}/messages`, { message })
  },
}
