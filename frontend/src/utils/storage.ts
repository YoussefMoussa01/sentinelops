export const getStorageItem = (key: string): string | null => {
  try {
    return localStorage.getItem(key)
  } catch {
    return null
  }
}

export const setStorageItem = (key: string, value: string): void => {
  try {
    localStorage.setItem(key, value)
  } catch {
    console.warn(`Failed to set localStorage item: ${key}`)
  }
}

export const removeStorageItem = (key: string): void => {
  try {
    localStorage.removeItem(key)
  } catch {
    console.warn(`Failed to remove localStorage item: ${key}`)
  }
}

export const clearStorage = (): void => {
  try {
    localStorage.clear()
  } catch {
    console.warn('Failed to clear localStorage')
  }
}
