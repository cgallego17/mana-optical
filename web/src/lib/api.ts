// En dev el proxy de Vite reenvía /api → http://127.0.0.1:8000/api
// En producción se puede sobreescribir con VITE_API_BASE_URL
const DEFAULT_API_BASE_URL = '/api'

export function getApiBaseUrl(): string {
  const envUrl = import.meta.env.VITE_API_BASE_URL as string | undefined
  return (envUrl && envUrl.trim()) ? envUrl.replace(/\/+$/, '') : DEFAULT_API_BASE_URL
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
    let detail = ''
    try {
      const data = await res.json()
      detail = (data?.detail as string) || JSON.stringify(data)
    } catch {
      detail = await res.text()
    }
    throw new Error(detail || `HTTP ${res.status}`)
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

export async function apiFetchAuth<T>(path: string, accessToken: string, init?: RequestInit): Promise<T> {
  return apiFetch<T>(path, {
    ...(init ?? {}),
    headers: {
      ...(init?.headers ?? {}),
      Authorization: `Bearer ${accessToken}`,
    },
  })
}
