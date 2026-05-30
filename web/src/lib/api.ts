const DEFAULT_API_BASE_URL = 'http://127.0.0.1:8000/api'

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

  return res.json() as Promise<T>
}
