import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(),
  scrollBehavior: () => ({ top: 0, behavior: 'smooth' }),
  routes: [
    { path: '/',         name: 'inicio',   component: HomeView },
    { path: '/servicios',name: 'servicios',component: () => import('../views/ServiciosView.vue') },
    { path: '/tienda',   name: 'tienda',   component: () => import('../views/TiendaView.vue') },
    { path: '/producto/:slug', name: 'producto', component: () => import('../views/ProductoView.vue') },
    { path: '/blog',     name: 'blog',     component: () => import('../views/BlogView.vue') },
    { path: '/nosotros', name: 'nosotros', component: () => import('../views/NosotrosView.vue') },
    { path: '/paginas',  name: 'paginas',  component: () => import('../views/PaginasView.vue') },
    { path: '/agenda',   name: 'agenda',   component: () => import('../views/AgendaView.vue') },
    { path: '/contacto', name: 'contacto', component: () => import('../views/ContactoView.vue') },
    { path: '/galeria',  name: 'galeria',  component: () => import('../views/GaleriaView.vue') },
    { path: '/buscar',   redirect: '/' },
    { path: '/cuenta',   name: 'cuenta',   component: () => import('../views/CuentaView.vue') },
    { path: '/carrito',  name: 'carrito',  component: () => import('../views/CarritoView.vue') },
    { path: '/:pathMatch(.*)*', name: 'not-found', component: () => import('../views/NotFoundView.vue') },
  ],
})

export default router
