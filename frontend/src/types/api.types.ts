export interface ApiResponse<T = unknown> {
  status: 'success' | 'error'
  data?: T
  error?: {
    code: string
    message: string
    details?: unknown
  }
  meta: {
    timestamp: string
  }
}

export interface PaginatedResponse<T> extends ApiResponse<T[]> {
  meta: {
    timestamp: string
    pagination: {
      page: number
      page_size: number
      total: number
      total_pages: number
    }
  }
}

export interface Pagination {
  page: number
  pageSize: number
  total: number
  totalPages: number
}
