const SITE_NAME = 'Maná Óptical'
const DEFAULT_IMAGE = '/logo.png'
const SITE_URL = typeof window !== 'undefined' ? window.location.origin : 'https://manaoptical.com'

function setMeta(attr: 'name' | 'property', key: string, value: string) {
  const sel = `meta[${attr}="${key}"]`
  let el = document.querySelector<HTMLMetaElement>(sel)
  if (!el) {
    el = document.createElement('meta')
    el.setAttribute(attr, key)
    document.head.appendChild(el)
  }
  el.setAttribute('content', value)
}

function setCanonical(href: string) {
  let el = document.querySelector<HTMLLinkElement>('link[rel="canonical"]')
  if (!el) {
    el = document.createElement('link')
    el.setAttribute('rel', 'canonical')
    document.head.appendChild(el)
  }
  el.href = href
}

function setJsonLd(id: string, data: Record<string, unknown>) {
  let el = document.getElementById(id) as HTMLScriptElement | null
  if (!el) {
    el = document.createElement('script')
    el.id = id
    el.type = 'application/ld+json'
    document.head.appendChild(el)
  }
  el.textContent = JSON.stringify(data)
}

export function removeJsonLd(id: string) {
  document.getElementById(id)?.remove()
}

export interface SeoOptions {
  title: string
  description?: string
  image?: string
  type?: 'website' | 'article' | 'product'
  jsonLd?: { id: string; data: Record<string, unknown> }
}

export function useSeo() {
  function setPage(opts: SeoOptions) {
    const title = `${opts.title} | ${SITE_NAME}`
    const desc  = opts.description ?? ''
    const img   = opts.image ?? DEFAULT_IMAGE
    const url   = typeof window !== 'undefined' ? window.location.href : SITE_URL

    document.title = opts.title.includes(SITE_NAME) ? opts.title : title

    setMeta('name', 'description', desc)

    // Open Graph
    setMeta('property', 'og:site_name',  SITE_NAME)
    setMeta('property', 'og:type',        opts.type ?? 'website')
    setMeta('property', 'og:title',       title)
    setMeta('property', 'og:description', desc)
    setMeta('property', 'og:image',       img)
    setMeta('property', 'og:url',         url)

    // Twitter Card
    setMeta('name', 'twitter:card',        'summary_large_image')
    setMeta('name', 'twitter:title',       title)
    setMeta('name', 'twitter:description', desc)
    setMeta('name', 'twitter:image',       img)

    setCanonical(url)

    if (opts.jsonLd) setJsonLd(opts.jsonLd.id, opts.jsonLd.data)
  }

  /** JSON-LD para la organización/negocio (se inserta una sola vez) */
  function setOrganization() {
    setJsonLd('ld-organization', {
      '@context': 'https://schema.org',
      '@type': 'LocalBusiness',
      '@id': SITE_URL,
      name: SITE_NAME,
      description: 'Óptica premium: exámenes visuales, monturas y asesoría.',
      image: `${SITE_URL}/logo.png`,
      telephone: '+573005262309',
      email: 'manaoptical2@gmail.com',
      url: SITE_URL,
      address: {
        '@type': 'PostalAddress',
        streetAddress: 'Calle 19 #19-06',
        addressLocality: 'Betania',
        addressRegion: 'Antioquia',
        addressCountry: 'CO',
      },
      openingHoursSpecification: [{
        '@type': 'OpeningHoursSpecification',
        dayOfWeek: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
        opens: '09:00',
        closes: '21:00',
      }],
      sameAs: [
        'https://www.facebook.com/manaoptical',
        'https://www.instagram.com/manaoptical',
      ],
    })
  }

  /** JSON-LD para un producto */
  function setProduct(p: {
    nombre: string; descripcion: string; imagen: string; precio: number
    precioAnterior: number | null; marca: string; slug: string
  }) {
    setJsonLd('ld-product', {
      '@context': 'https://schema.org',
      '@type': 'Product',
      name: p.nombre,
      description: p.descripcion,
      image: p.imagen,
      brand: { '@type': 'Brand', name: p.marca },
      url: `${SITE_URL}/producto/${p.slug}`,
      offers: {
        '@type': 'Offer',
        priceCurrency: 'COP',
        price: p.precio,
        priceValidUntil: new Date(Date.now() + 30 * 86400000).toISOString().split('T')[0],
        availability: 'https://schema.org/InStock',
        seller: { '@type': 'Organization', name: SITE_NAME },
        ...(p.precioAnterior ? { priceSpecification: {
          '@type': 'UnitPriceSpecification',
          price: p.precioAnterior,
          priceCurrency: 'COP',
        }} : {}),
      },
    })
  }

  /** JSON-LD para un artículo de blog */
  function setBlogPost(post: {
    titulo: string; extracto: string; imagen: string
    slug: string; fecha: string
  }) {
    setJsonLd('ld-blogpost', {
      '@context': 'https://schema.org',
      '@type': 'BlogPosting',
      headline: post.titulo,
      description: post.extracto,
      image: post.imagen,
      datePublished: post.fecha,
      url: `${SITE_URL}/blog/${post.slug}`,
      author: { '@type': 'Organization', name: SITE_NAME },
      publisher: {
        '@type': 'Organization',
        name: SITE_NAME,
        logo: { '@type': 'ImageObject', url: `${SITE_URL}/logo.png` },
      },
    })
  }

  /** Breadcrumb JSON-LD */
  function setBreadcrumb(items: { name: string; url: string }[]) {
    setJsonLd('ld-breadcrumb', {
      '@context': 'https://schema.org',
      '@type': 'BreadcrumbList',
      itemListElement: items.map((item, i) => ({
        '@type': 'ListItem',
        position: i + 1,
        name: item.name,
        item: item.url,
      })),
    })
  }

  return { setPage, setOrganization, setProduct, setBlogPost, setBreadcrumb }
}
