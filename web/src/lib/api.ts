// En dev el proxy de Vite reenvía /api → http://127.0.0.1:8000/api
// En producción se puede sobreescribir con VITE_API_BASE_URL
const DEFAULT_API_BASE_URL = '/api'

export function getApiBaseUrl(): string {
  const envUrl = import.meta.env.VITE_API_BASE_URL as string | undefined
  return (envUrl && envUrl.trim()) ? envUrl.replace(/\/+$/, '') : DEFAULT_API_BASE_URL
}

export class ApiError extends Error {
  status: number
  constructor(message: string, status: number) {
    super(message)
    this.status = status
  }
}

export async function apiFetch<T>(path: string, init?: RequestInit): Promise<T> {
  const base = getApiBaseUrl()
  const url = `${base}${path.startsWith('/') ? '' : '/'}${path}`

  const res = await fetch(url, {
    ...init,
    headers: {
      'Content-Type': 'application/json',
      ...(init?.headers ?? {}),
    },
  })

  if (!res.ok) {
    const raw = await res.text()
    let detail = raw
    try {
      const data = JSON.parse(raw)
      detail = (data?.detail as string) || JSON.stringify(data)
    } catch {
      // raw no era JSON (ej. página de error HTML) — se usa tal cual.
    }
    throw new ApiError(detail || `HTTP ${res.status}`, res.status)
  }

  const contentType = res.headers.get('content-type') || ''
  if (!contentType.includes('application/json')) {
    const text = await res.text()
    const head = text.slice(0, 120).replace(/\s+/g, ' ').trim()
    throw new Error(`Respuesta no-JSON (${res.status}) desde ${url}: ${head}`)
  }

  return res.json() as Promise<T>
}

export function unwrapResults<T>(data: T[] | { results: T[] } | null | undefined): T[] {
  if (!data) return []
  if (Array.isArray(data)) return data
  if (typeof data === 'object' && 'results' in data && Array.isArray((data as any).results)) {
    return (data as any).results as T[]
  }
  return []
}

let refreshPromise: Promise<string | null> | null = null

// Evita disparar varios refresh en paralelo cuando varias llamadas 401 a la vez
function refreshAccessToken(): Promise<string | null> {
  if (!refreshPromise) {
    refreshPromise = (async () => {
      const { useAuth } = await import('../composables/auth')
      const auth = useAuth()
      try {
        await auth.refresh()
        return auth.getAccessToken()
      } catch {
        auth.logout()
        return null
      }
    })().finally(() => {
      refreshPromise = null
    })
  }
  return refreshPromise
}

export async function apiFetchAuth<T>(path: string, accessToken: string, init?: RequestInit): Promise<T> {
  const withToken = (token: string) => apiFetch<T>(path, {
    ...(init ?? {}),
    headers: {
      ...(init?.headers ?? {}),
      Authorization: `Bearer ${token}`,
    },
  })

  try {
    return await withToken(accessToken)
  } catch (err) {
    if (!(err instanceof ApiError) || err.status !== 401) throw err

    const newToken = await refreshAccessToken()
    if (newToken) return withToken(newToken)

    if (typeof window !== 'undefined' && window.location.pathname !== '/panel/login') {
      window.location.href = '/panel/login'
    }
    throw err
  }
}
