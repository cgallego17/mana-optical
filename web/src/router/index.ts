import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import { useAuth } from '../composables/auth'

const router = createRouter({
  history: createWebHistory(),
  scrollBehavior: () => ({ top: 0, behavior: 'smooth' }),
  routes: [
    { path: '/',          name: 'inicio',    meta: { title: 'Maná Óptical — Visión con Propósito', description: 'Óptica premium: exámenes visuales, monturas y asesoría en Betania, Antioquia.' }, component: HomeView },
    { path: '/servicios', name: 'servicios', meta: { title: 'Servicios | Maná Óptical', description: 'Examen visual completo, terapia visual y asesoría en monturas con especialistas.' }, component: () => import('../views/ServiciosView.vue') },
    { path: '/tienda',    name: 'tienda',    meta: { title: 'Tienda | Maná Óptical', description: 'Explora nuestro catálogo de monturas, gafas de sol, lentes de contacto y accesorios.' }, component: () => import('../views/TiendaView.vue') },
    { path: '/producto/:slug',  name: 'producto',  component: () => import('../views/ProductoView.vue') },
    { path: '/categoria/:slug', name: 'categoria', component: () => import('../views/CategoriaView.vue') },
    { path: '/blog',      name: 'blog',      meta: { title: 'Blog | Maná Óptical', description: 'Consejos de salud visual, estilo óptico y tendencias en monturas.' }, component: () => import('../views/BlogView.vue') },
    { path: '/blog/:slug',name: 'blog-post', component: () => import('../views/BlogPostView.vue') },
    { path: '/nosotros',  name: 'nosotros',  meta: { title: 'Nosotros | Maná Óptical', description: 'Conoce al equipo de Maná Óptical, óptica premium en Betania, Antioquia.' }, component: () => import('../views/NosotrosView.vue') },
    { path: '/paginas',   name: 'paginas',   meta: { title: 'Páginas | Maná Óptical' }, component: () => import('../views/PaginasView.vue') },
    { path: '/agenda',    name: 'agenda',    meta: { title: 'Agenda tu Cita | Maná Óptical', description: 'Reserva tu cita de examen visual con nuestros especialistas. Confirmación inmediata.' }, component: () => import('../views/AgendaView.vue') },
    { path: '/contacto',  name: 'contacto',  meta: { title: 'Contacto | Maná Óptical', description: 'Contáctanos en Calle 19 #19-06, Betania, Antioquia. WhatsApp: 300 526 2309.' }, component: () => import('../views/ContactoView.vue') },
    { path: '/galeria',   name: 'galeria',   meta: { title: 'Galería | Maná Óptical', description: 'Galería de monturas, instalaciones y momentos de nuestra óptica.' }, component: () => import('../views/GaleriaView.vue') },
    { path: '/buscar',    redirect: '/' },
    { path: '/cuenta',    name: 'cuenta',    component: () => import('../views/CuentaView.vue') },
    { path: '/carrito',   name: 'carrito',   component: () => import('../views/CarritoView.vue') },

    { path: '/panel/login', name: 'admin-login', meta: { title: 'Panel | Login' }, component: () => import('../views/AdminLoginView.vue') },
    {
      path: '/panel',
      meta: { requiresAuth: true },
      component: () => import('../views/AdminView.vue'),
      children: [
        { path: '',          redirect: 'dashboard' },
        { path: 'dashboard', name: 'admin-dashboard', component: () => import('../views/admin/AdminDashboard.vue') },
        { path: 'productos', name: 'admin-productos',  component: () => import('../views/admin/AdminProductos.vue') },
        { path: 'categorias',name: 'admin-categorias', component: () => import('../views/admin/AdminCategorias.vue') },
        { path: 'marcas',    name: 'admin-marcas',     component: () => import('../views/admin/AdminMarcas.vue') },
        { path: 'blog',      name: 'admin-blog',       component: () => import('../views/admin/AdminBlog.vue') },
        { path: 'reservas',  name: 'admin-reservas',   component: () => import('../views/admin/AdminReservas.vue') },
        { path: 'servicios', name: 'admin-servicios',  component: () => import('../views/admin/AdminServicios.vue') },
      ],
    },

    { path: '/:pathMatch(.*)*', name: 'not-found', component: () => import('../views/NotFoundView.vue') },
  ],
})

// Proteger rutas admin
router.beforeEach((to) => {
  const requiresAuth = to.matched.some(r => r.meta?.requiresAuth)
  if (!requiresAuth) return true
  const { isAuthenticated } = useAuth()
  if (isAuthenticated.value) return true
  return { name: 'admin-login' }
})

// SEO: actualizar title, description y OG/Twitter en cada navegación
function setMetaAttr(attr: string, key: string, value: string) {
  const sel = `meta[${attr}="${key}"]`
  let el = document.querySelector<HTMLMetaElement>(sel)
  if (!el) {
    el = document.createElement('meta')
    el.setAttribute(attr, key)
    document.head.appendChild(el)
  }
  el.setAttribute('content', value)
}

router.afterEach((to) => {
  const meta = to.meta as { title?: string; description?: string } | undefined
  const title = meta?.title ?? 'Maná Óptical — Visión con Propósito'
  const desc  = meta?.description ?? 'Óptica premium: exámenes visuales, monturas y asesoría.'
  const url   = typeof window !== 'undefined' ? window.location.href : ''

  document.title = title

  setMetaAttr('name',     'description',       desc)
  setMetaAttr('property', 'og:title',          title)
  setMetaAttr('property', 'og:description',    desc)
  setMetaAttr('property', 'og:url',            url)
  setMetaAttr('name',     'twitter:title',     title)
  setMetaAttr('name',     'twitter:description', desc)

  // Canonical
  let canonical = document.querySelector<HTMLLinkElement>('link[rel="canonical"]')
  if (!canonical) {
    canonical = document.createElement('link')
    canonical.setAttribute('rel', 'canonical')
    document.head.appendChild(canonical)
  }
  canonical.href = url
})

export default router
