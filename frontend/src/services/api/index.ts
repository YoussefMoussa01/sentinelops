// Auth API
// TODO: Implement in Phase 3
export const authAPI = {
  login: async (username: string, password: string) => {
    // return apiClient.post('/auth/login', { username, password })
  },
  logout: async () => {
    // return apiClient.post('/auth/logout', {})
  },
  getCurrentUser: async () => {
    // return apiClient.get('/auth/me')
  },
  refreshToken: async () => {
    // return apiClient.post('/auth/refresh', {})
  },
}

// Alerts API
// TODO: Implement in Phase 4
export const alertsAPI = {
  getAlerts: async () => {
    // return apiClient.get('/alerts')
  },
  getAlert: async (id: string) => {
    // return apiClient.get(`/alerts/${id}`)
  },
  updateAlert: async (id: string, data: unknown) => {
    // return apiClient.patch(`/alerts/${id}`, data)
  },
}

// Investigations API
// TODO: Implement in Phase 4
export const investigationsAPI = {
  getInvestigations: async () => {
    // return apiClient.get('/investigations')
  },
  getInvestigation: async (id: string) => {
    // return apiClient.get(`/investigations/${id}`)
  },
  createInvestigation: async (data: unknown) => {
    // return apiClient.post('/investigations', data)
  },
  updateInvestigation: async (id: string, data: unknown) => {
    // return apiClient.patch(`/investigations/${id}`, data)
  },
}

// Users API
// TODO: Implement in Phase 4
export const usersAPI = {
  getUsers: async () => {
    // return apiClient.get('/users')
  },
  getUser: async (id: string) => {
    // return apiClient.get(`/users/${id}`)
  },
}

// Devices API
// TODO: Implement in Phase 4
export const devicesAPI = {
  getDevices: async () => {
    // return apiClient.get('/devices')
  },
  getDevice: async (id: string) => {
    // return apiClient.get(`/devices/${id}`)
  },
}

// Logs API
// TODO: Implement in Phase 4
export const logsAPI = {
  getLogs: async () => {
    // return apiClient.get('/logs')
  },
  searchLogs: async (query: string) => {
    // return apiClient.get('/logs/search', { query })
  },
}

// AI API
// TODO: Implement in Phase 8
export const aiAPI = {
  getConversations: async () => {
    // return apiClient.get('/ai/conversations')
  },
  getConversation: async (id: string) => {
    // return apiClient.get(`/ai/conversations/${id}`)
  },
  createConversation: async (data: unknown) => {
    // return apiClient.post('/ai/conversations', data)
  },
  sendMessage: async (conversationId: string, message: string) => {
    // return apiClient.post(`/ai/conversations/${conversationId}/messages`, { message })
  },
}
