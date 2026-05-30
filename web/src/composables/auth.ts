import { ref, computed } from 'vue'

import { apiFetch } from '../lib/api'

type TokenResponse = {
  access: string
  refresh: string
}

const ACCESS_KEY = 'mana_access_token'
const REFRESH_KEY = 'mana_refresh_token'

const accessToken = ref<string | null>(typeof window !== 'undefined' ? localStorage.getItem(ACCESS_KEY) : null)
const refreshToken = ref<string | null>(typeof window !== 'undefined' ? localStorage.getItem(REFRESH_KEY) : null)

export function useAuth() {
  const isAuthenticated = computed(() => Boolean(accessToken.value))

  function setTokens(tokens: TokenResponse) {
    accessToken.value = tokens.access
    refreshToken.value = tokens.refresh
    localStorage.setItem(ACCESS_KEY, tokens.access)
    localStorage.setItem(REFRESH_KEY, tokens.refresh)
  }

  function clearTokens() {
    accessToken.value = null
    refreshToken.value = null
    localStorage.removeItem(ACCESS_KEY)
    localStorage.removeItem(REFRESH_KEY)
  }

  async function login(username: string, password: string) {
    const tokens = await apiFetch<TokenResponse>('/auth/token/', {
      method: 'POST',
      body: JSON.stringify({ username, password }),
    })
    setTokens(tokens)
  }

  async function refresh() {
    if (!refreshToken.value) throw new Error('No refresh token')
    const tokens = await apiFetch<{ access: string }>('/auth/refresh/', {
      method: 'POST',
      body: JSON.stringify({ refresh: refreshToken.value }),
    })
    accessToken.value = tokens.access
    localStorage.setItem(ACCESS_KEY, tokens.access)
  }

  function logout() {
    clearTokens()
  }

  function getAccessToken() {
    return accessToken.value
  }

  return {
    isAuthenticated,
    login,
    refresh,
    logout,
    getAccessToken,
  }
}
