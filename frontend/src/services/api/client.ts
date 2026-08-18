import axios, { AxiosInstance, AxiosError } from 'axios'
import { ApiResponse } from '@/types/api.types'

class ApiClient {
  private client: AxiosInstance

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

    // Handle 401 responses
    this.client.interceptors.response.use(
      (response) => response,
      (error: AxiosError) => {
        if (error.response?.status === 401) {
          // Clear tokens on unauthorized
          localStorage.removeItem(
            import.meta.env.VITE_TOKEN_STORAGE_KEY || 'sentinelops_token'
          )
          localStorage.removeItem('sentinelops_refresh_token')
          // Redirect to login
          window.location.href = '/login'
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

  private handleError(error: unknown) {
    if (axios.isAxiosError(error)) {
      const message = error.response?.data?.error?.message || 
                      error.response?.statusText || 
                      error.message ||
                      'API error'
      return new Error(message)
    }
    return error instanceof Error ? error : new Error('Unknown error')
  }
}

export const apiClient = new ApiClient()
