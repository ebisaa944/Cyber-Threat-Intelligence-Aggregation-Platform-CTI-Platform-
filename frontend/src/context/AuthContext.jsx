import { createContext, useEffect, useState } from 'react'
import api, { fetchProfile, saveTokens } from '../api'

export const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    let mounted = true
    async function init() {
      const access = localStorage.getItem('access_token')
      if (access) {
        const profile = await fetchProfile()
        if (mounted) setUser(profile)
      }
      if (mounted) setLoading(false)
    }
    init()
    return () => { mounted = false }
  }, [])

  async function login({ username, password }) {
    const resp = await api.post('auth/token/', { username, password })
    saveTokens(resp.data)
    const profile = await fetchProfile()
    setUser(profile)
    return profile
  }

  function logout() {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{ user, loading, login, logout }}>
      {children}
    </AuthContext.Provider>
  )
}
