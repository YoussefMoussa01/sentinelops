export const getEnvVar = (key: string, defaultValue?: string): string => {
  const value = import.meta.env[key]
  if (!value && !defaultValue) {
    throw new Error(`Environment variable ${key} not found`)
  }
  return value || defaultValue || ''
}
