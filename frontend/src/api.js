import axios from 'axios'

const API_BASE = (typeof process !== 'undefined' && process.env && process.env.VITE_API_BASE_URL)
  ? process.env.VITE_API_BASE_URL
  : '/api/';

const api = axios.create({
  baseURL: API_BASE,
})

function getAccess() {
  return localStorage.getItem('access_token')
}

function getRefresh() {
  return localStorage.getItem('refresh_token')
}

export async function refreshToken() {
  const refresh = getRefresh()
  if (!refresh) return null
  try {
    const resp = await api.post('auth/token/refresh/', { refresh })
    localStorage.setItem('access_token', resp.data.access)
    return resp.data.access
  } catch (err) {
    console.error('refresh failed', err)
    return null
  }
}

api.interceptors.request.use((config) => {
  const token = getAccess()
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

api.interceptors.response.use(
  (res) => res,
  async (error) => {
    console.error('API response error', error.response?.status, error.response?.data)
    const original = error.config
    if (error.response && error.response.status === 401 && !original._retry) {
      original._retry = true
      const newAccess = await refreshToken()
      if (newAccess) {
        original.headers.Authorization = `Bearer ${newAccess}`
        return api(original)
      }
    }
    return Promise.reject(error)
  }
)

export function saveTokens({ access, refresh }) {
  if (access) localStorage.setItem('access_token', access)
  if (refresh) localStorage.setItem('refresh_token', refresh)
}

export function logout() {
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
}

export default api

export async function fetchProfile() {
  try {
    const resp = await api.get('auth/profile/')
    return resp.data
  } catch (err) {
    return null
  }
}
