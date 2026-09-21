import axios, { AxiosInstance, AxiosError, InternalAxiosRequestConfig } from 'axios'

class ApiClient {
  private client: AxiosInstance
  private refreshPromise: Promise<string> | null = null

  constructor() {
    this.client = axios.create({
      baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1',
      headers: {
        'Content-Type': 'application/json',
      },
    })

    // Add token to requests
    this.client.interceptors.request.use((config) => {
      const token = localStorage.getItem(
        import.meta.env.VITE_TOKEN_STORAGE_KEY || 'sentinelops_token'
      )
      if (token && config.url !== '/auth/login') {
        config.headers.Authorization = `Bearer ${token}`
      }
      return config
    })

    // Refresh an expired access token once before ending the session.
    this.client.interceptors.response.use(
      (response) => response,
      async (error: AxiosError) => {
        const originalRequest = error.config as (InternalAxiosRequestConfig & { _retry?: boolean }) | undefined
        const isRefreshRequest = originalRequest?.url?.includes('/auth/refresh')
        const tokenKey = import.meta.env.VITE_TOKEN_STORAGE_KEY || 'sentinelops_token'
        const refreshToken = localStorage.getItem('sentinelops_refresh_token')

        if (error.response?.status === 401 && originalRequest && !originalRequest._retry && !isRefreshRequest && refreshToken) {
          originalRequest._retry = true
          try {
            this.refreshPromise ??= this.client
              .post<{ access_token: string; refresh_token?: string }>('/auth/refresh', { refresh_token: refreshToken })
              .then(({ data }) => {
                localStorage.setItem(tokenKey, data.access_token)
                if (data.refresh_token) localStorage.setItem('sentinelops_refresh_token', data.refresh_token)
                return data.access_token
              })
              .finally(() => { this.refreshPromise = null })

            const accessToken = await this.refreshPromise
            originalRequest.headers.Authorization = `Bearer ${accessToken}`
            return this.client.request(originalRequest)
          } catch {
            // Fall through to the normal session cleanup below.
          }
        }

        if (error.response?.status === 401) {
          localStorage.removeItem(tokenKey)
          localStorage.removeItem('sentinelops_refresh_token')
          if (window.location.pathname !== '/login') window.location.href = '/login'
        }
        return Promise.reject(error)
      }
    )
  }

  async get<T>(path: string, params?: Record<string, unknown>) {
    try {
      const response = await this.client.get<T>(path, { params })
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  async getWithTotal<T>(path: string, params?: object): Promise<{ items: T; total: number }> {
    try {
      const response = await this.client.get<T>(path, { params })
      const header = response.headers['x-total-count']
      const data = response.data
      const total = header !== undefined ? Number(header) : Array.isArray(data) ? data.length : 0
      return { items: data, total: Number.isNaN(total) ? 0 : total }
    } catch (error) {
      throw this.handleError(error)
    }
  }

  async post<T, D = unknown>(path: string, data?: D) {
    try {
      const response = await this.client.post<T>(path, data)
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  async patch<T, D = unknown>(path: string, data?: D) {
    try {
      const response = await this.client.patch<T>(path, data)
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  async delete<T>(path: string) {
    try {
      const response = await this.client.delete<T>(path)
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  async streamPost(path: string, data: unknown, onEvent: (event: { type: string; content?: string }) => void) {
    const tokenKey = import.meta.env.VITE_TOKEN_STORAGE_KEY || 'sentinelops_token'
    const response = await fetch(`${this.client.defaults.baseURL}${path}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${localStorage.getItem(tokenKey) || ''}` },
      body: JSON.stringify(data),
    })
    if (!response.ok || !response.body) throw new Error(response.statusText || 'Streaming request failed')
    const reader = response.body.getReader()
    const decoder = new TextDecoder()
    let buffer = ''
    while (true) {
      const { value, done } = await reader.read()
      buffer += decoder.decode(value || new Uint8Array(), { stream: !done })
      const events = buffer.split('\n\n')
      buffer = events.pop() || ''
      for (const event of events) {
        const line = event.split('\n').find((item) => item.startsWith('data: '))
        if (line) onEvent(JSON.parse(line.slice(6)) as { type: string; content?: string })
      }
      if (done) break
    }
  }

  private handleError(error: unknown) {
    if (axios.isAxiosError(error)) {
      const responseData = error.response?.data as { detail?: string | { message?: string }; error?: { message?: string } } | undefined
      const message = (typeof responseData?.detail === 'string' ? responseData.detail : responseData?.detail?.message) ||
                      responseData?.error?.message ||
                      error.response?.statusText || 
                      error.message ||
                      'API error'
      return new Error(message)
    }
    return error instanceof Error ? error : new Error('Unknown error')
  }
}

export const apiClient = new ApiClient()
