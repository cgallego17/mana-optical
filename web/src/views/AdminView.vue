<script setup lang="ts">
import { ref } from 'vue'
import { RouterLink, RouterView, useRouter } from 'vue-router'
import {
  LayoutDashboard, Package, Tag, Award, FileText,
  Calendar, Clock, CalendarClock, LogOut, Menu, X
} from 'lucide-vue-next'
import { useAuth } from '../composables/auth'

const router = useRouter()
const { logout } = useAuth()
const sidebarOpen = ref(false)

type NavItem =
  | { type: 'link'; to: string; name: string; icon: unknown; label: string }
  | { type: 'header'; label: string }

const nav: NavItem[] = [
  { type: 'link', to: '/panel/dashboard', name: 'admin-dashboard', icon: LayoutDashboard, label: 'Dashboard' },
  { type: 'header', label: 'Catálogo' },
  { type: 'link', to: '/panel/productos',  name: 'admin-productos',  icon: Package,  label: 'Productos' },
  { type: 'link', to: '/panel/categorias', name: 'admin-categorias', icon: Tag,      label: 'Categorías' },
  { type: 'link', to: '/panel/marcas',     name: 'admin-marcas',     icon: Award,    label: 'Marcas' },
  { type: 'header', label: 'Contenido' },
  { type: 'link', to: '/panel/blog',       name: 'admin-blog',       icon: FileText, label: 'Blog' },
  { type: 'header', label: 'Agenda' },
  { type: 'link', to: '/panel/reservas',   name: 'admin-reservas',   icon: Calendar, label: 'Reservas' },
  { type: 'link', to: '/panel/servicios',  name: 'admin-servicios',  icon: Clock,    label: 'Servicios' },
  { type: 'link', to: '/panel/horarios',   name: 'admin-horarios',   icon: CalendarClock, label: 'Horarios' },
]

function salir() {
  logout()
  router.push({ name: 'admin-login' })
}
</script>

<template>
  <div class="min-h-screen bg-[#0c110e] text-white flex">

    <!-- Sidebar overlay (móvil) -->
    <transition name="fade">
      <div
        v-if="sidebarOpen"
        class="fixed inset-0 z-[50] bg-black/60 lg:hidden"
        @click="sidebarOpen = false"
      />
    </transition>

    <!-- Sidebar -->
    <aside
      class="fixed left-0 top-0 z-[55] h-full w-60 bg-[#0f1612] border-r border-white/[0.07] flex flex-col
             transition-transform duration-250 lg:translate-x-0"
      :class="sidebarOpen ? 'translate-x-0' : '-translate-x-full'"
    >
      <!-- Logo -->
      <div class="px-5 py-6 border-b border-white/[0.07] shrink-0">
        <p class="text-[9px] tracking-[0.35em] uppercase text-[#f5d984]/70 mb-0.5">Panel Admin</p>
        <h1 class="text-base font-black uppercase tracking-wide" style="font-family:'Playfair Display',serif;">
          Maná Óptical
        </h1>
      </div>

      <!-- Nav -->
      <nav class="flex-1 overflow-y-auto py-4 px-3 space-y-0.5">
        <template v-for="item in nav" :key="'label' in item ? item.label : (item as any).to">
          <!-- Header de sección -->
          <p
            v-if="item.type === 'header'"
            class="px-3 pt-5 pb-1 text-[9px] font-black tracking-[0.28em] uppercase text-white/25"
          >{{ item.label }}</p>

          <!-- Link -->
          <RouterLink
            v-else
            :to="item.to"
            @click="sidebarOpen = false"
            class="flex items-center gap-3 px-3 py-2.5 rounded text-[12px] font-semibold tracking-wide transition-colors"
            :class="$route.path.startsWith(item.to)
              ? 'bg-white/10 text-[#f5d984]'
              : 'text-white/55 hover:text-white hover:bg-white/5'"
          >
            <component :is="item.icon" class="h-4 w-4 shrink-0" />
            {{ item.label }}
          </RouterLink>
        </template>
      </nav>

      <!-- Logout -->
      <div class="border-t border-white/[0.07] p-3 shrink-0">
        <button
          @click="salir"
          class="w-full flex items-center gap-3 px-3 py-2.5 rounded text-[12px] font-semibold text-white/40 hover:text-red-300 hover:bg-red-500/10 transition-colors"
        >
          <LogOut class="h-4 w-4 shrink-0" /> Cerrar sesión
        </button>
      </div>
    </aside>

    <!-- Área principal -->
    <div class="flex-1 flex flex-col min-h-screen lg:pl-60">

      <!-- Top bar (móvil) -->
      <header class="lg:hidden sticky top-0 z-40 flex items-center gap-4 border-b border-white/[0.07] bg-[#0f1612] px-4 py-3 shrink-0">
        <button @click="sidebarOpen = !sidebarOpen" class="p-1.5 rounded text-white/60 hover:text-white hover:bg-white/10 transition">
          <component :is="sidebarOpen ? X : Menu" class="h-5 w-5" />
        </button>
        <span class="text-sm font-bold uppercase tracking-wider">Admin</span>
      </header>

      <!-- Contenido de la sección activa -->
      <main class="flex-1 overflow-auto">
        <RouterView />
      </main>
    </div>
  </div>
</template>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity .2s ease }
.fade-enter-from, .fade-leave-to { opacity: 0 }
</style>
