import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(),
  scrollBehavior: () => ({ top: 0, behavior: 'smooth' }),
  routes: [
    { path: '/',         name: 'inicio',   component: HomeView },
    { path: '/tienda',   name: 'tienda',   component: () => import('../views/TiendaView.vue') },
    { path: '/blog',     name: 'blog',     component: () => import('../views/BlogView.vue') },
    { path: '/nosotros', name: 'nosotros', component: () => import('../views/NosotrosView.vue') },
    { path: '/paginas',  name: 'paginas',  component: () => import('../views/PaginasView.vue') },
  ],
})

export default router
