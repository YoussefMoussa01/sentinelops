import { useCallback, useEffect, useMemo, useState } from 'react'
import { useSearchParams } from 'react-router-dom'

export type SortDir = 'asc' | 'desc'

export interface ListFilters {
  search: string
  status: string
  severity: string
  sortBy: string
  sortDir: SortDir
  page: number
}

interface UseListQueryOptions {
  defaultSortBy?: string
  defaultSortDir?: SortDir
  pageSize?: number
  debounceMs?: number
}

interface QueryPatch {
  q?: string
  status?: string
  severity?: string
  sort?: string
  dir?: SortDir
  page?: number
}

/**
 * Keeps list search, filters, sorting and pagination in the URL so views are
 * shareable and survive back/forward navigation.
 */
export function useListQuery({
  defaultSortBy = 'created_at',
  defaultSortDir = 'desc',
  pageSize = 20,
  debounceMs = 350,
}: UseListQueryOptions = {}) {
  const [searchParams, setSearchParams] = useSearchParams()

  const filters = useMemo<ListFilters>(() => {
    const dir = searchParams.get('dir')
    return {
      search: searchParams.get('q') ?? '',
      status: searchParams.get('status') ?? 'ALL',
      severity: searchParams.get('severity') ?? 'ALL',
      sortBy: searchParams.get('sort') ?? defaultSortBy,
      sortDir: dir === 'asc' || dir === 'desc' ? dir : defaultSortDir,
      page: Math.max(0, Number.parseInt(searchParams.get('page') ?? '0', 10) || 0),
    }
  }, [searchParams, defaultSortBy, defaultSortDir])

  const setParams = useCallback((patch: QueryPatch) => {
    setSearchParams((current) => {
      const next = new URLSearchParams(current)
      Object.entries(patch).forEach(([key, value]) => {
        const isDefault =
          value === undefined ||
          value === '' ||
          value === 'ALL' ||
          (key === 'page' && Number(value) === 0) ||
          (key === 'sort' && value === defaultSortBy) ||
          (key === 'dir' && value === defaultSortDir)
        if (isDefault) next.delete(key)
        else next.set(key, String(value))
      })
      return next
    }, { replace: true })
  }, [setSearchParams, defaultSortBy, defaultSortDir])

  const [searchInput, setSearchInput] = useState(filters.search)

  useEffect(() => {
    setSearchInput(filters.search)
  }, [filters.search])

  useEffect(() => {
    if (searchInput === filters.search) return
    const timer = setTimeout(() => setParams({ q: searchInput, page: 0 }), debounceMs)
    return () => clearTimeout(timer)
  }, [searchInput, filters.search, setParams, debounceMs])

  const toggleSort = useCallback((sortBy: string) => {
    const nextDir: SortDir = filters.sortBy === sortBy && filters.sortDir === 'desc' ? 'asc' : 'desc'
    setParams({ sort: sortBy, dir: nextDir, page: 0 })
  }, [filters.sortBy, filters.sortDir, setParams])

  return {
    filters,
    searchInput,
    setSearch: setSearchInput,
    setStatus: useCallback((status: string) => setParams({ status, page: 0 }), [setParams]),
    setSeverity: useCallback((severity: string) => setParams({ severity, page: 0 }), [setParams]),
    setPage: useCallback((page: number) => setParams({ page }), [setParams]),
    toggleSort,
    pageSize,
  }
}
