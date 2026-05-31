const CACHE = 'mana-v3'
const PRECACHE = ['/', '/index.html']

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE).then(c => c.addAll(PRECACHE).catch(() => {}))
  )
  self.skipWaiting()
})

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))
    )
  )
  self.clients.claim()
})

self.addEventListener('fetch', e => {
  const { request } = e
  const url = new URL(request.url)

  // Ignorar: no-GET, otros orígenes, API, panel de admin
  if (
    request.method !== 'GET' ||
    url.origin !== self.location.origin ||
    url.pathname.startsWith('/api/') ||
    url.pathname.startsWith('/panel/') ||
    url.pathname.startsWith('/django-admin/')
  ) return

  // Navegación (HTML): network-first, fallback al index.html en caché
  if (request.mode === 'navigate') {
    e.respondWith(
      fetch(request)
        .then(res => {
          if (res.ok) {
            const clone = res.clone()
            caches.open(CACHE).then(c => c.put(request, clone))
          }
          return res
        })
        .catch(() => caches.match('/index.html').then(r => r || Response.error()))
    )
    return
  }

  // Assets estáticos (JS, CSS, imágenes, fuentes): cache-first con fallback silencioso
  if (/\.(js|css|png|jpg|jpeg|svg|webp|woff2?|ico)(\?.*)?$/.test(url.pathname)) {
    e.respondWith(
      caches.match(request).then(cached => {
        if (cached) return cached
        return fetch(request)
          .then(res => {
            if (res.ok) {
              const clone = res.clone()
              caches.open(CACHE).then(c => c.put(request, clone))
            }
            return res
          })
          .catch(() => Response.error())
      })
    )
  }
})
