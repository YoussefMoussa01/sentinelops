export const validateEmail = (email: string): boolean => {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return re.test(email)
}

export const validateUsername = (username: string): boolean => {
  return username.length >= 3 && username.length <= 50
}

export const validatePassword = (password: string): boolean => {
  return password.length >= 8
}
