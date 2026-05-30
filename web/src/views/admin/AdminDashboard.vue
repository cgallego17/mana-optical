<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Package, FileText, Calendar, Clock } from 'lucide-vue-next'
import { apiFetchAuth } from '../../lib/api'
import { useAuth } from '../../composables/auth'

const { getAccessToken } = useAuth()

type KPI = { label: string; value: string | number; icon: unknown; color: string }

const kpis = ref<KPI[]>([
  { label: 'Productos',          value: '—', icon: Package,  color: 'text-[#f5d984]' },
  { label: 'Posts publicados',   value: '—', icon: FileText, color: 'text-emerald-400' },
  { label: 'Reservas totales',   value: '—', icon: Calendar, color: 'text-sky-400' },
  { label: 'Reservas pendientes',value: '—', icon: Clock,    color: 'text-amber-400' },
])

type ProductosRes  = { count?: number; results?: unknown[] }
type PostAdmin     = { publicado: boolean }
type ReservaAdmin  = { estado: string }

async function cargar() {
  const token = getAccessToken()
  if (!token) return

  const [productos, posts, reservas] = await Promise.allSettled([
    apiFetchAuth<ProductosRes>('/catalogo/productos/?page_size=1', token),
    apiFetchAuth<PostAdmin[]>('/blog/admin/posts/', token),
    apiFetchAuth<ReservaAdmin[]>('/agenda/admin/reservas/', token),
  ])

  if (productos.status === 'fulfilled') {
    const res = productos.value
    kpis.value[0].value = res.count ?? res.results?.length ?? '—'
  }
  if (posts.status === 'fulfilled') {
    kpis.value[1].value = posts.value.filter(p => p.publicado).length
  }
  if (reservas.status === 'fulfilled') {
    const res = reservas.value
    kpis.value[2].value = res.length
    kpis.value[3].value = res.filter(r => r.estado === 'pendiente').length
  }
}

onMounted(cargar)
</script>

<template>
  <div class="p-6 lg:p-10 max-w-5xl">
    <div class="mb-8">
      <p class="text-[10px] tracking-[0.35em] uppercase text-[#f5d984]/70 mb-1">Panel</p>
      <h2 class="text-2xl font-black uppercase tracking-tight" style="font-family:'Playfair Display',serif;">Dashboard</h2>
    </div>

    <!-- KPIs -->
    <div class="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-10">
      <div
        v-for="kpi in kpis" :key="kpi.label"
        class="bg-white/5 border border-white/[0.07] p-5 rounded"
      >
        <div class="flex items-center justify-between mb-3">
          <p class="text-[10px] tracking-widest uppercase text-white/35">{{ kpi.label }}</p>
          <component :is="kpi.icon" class="h-4 w-4" :class="kpi.color" />
        </div>
        <p class="text-3xl font-black" :class="kpi.color">{{ kpi.value }}</p>
      </div>
    </div>

    <!-- Accesos rápidos -->
    <div>
      <p class="text-[10px] tracking-widest uppercase text-white/30 mb-4">Acceso rápido</p>
      <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-3">
        <RouterLink
          v-for="link in [
            { to: '/admin/productos',  label: 'Gestionar productos' },
            { to: '/admin/reservas',   label: 'Ver reservas' },
            { to: '/admin/blog',       label: 'Gestionar blog' },
            { to: '/admin/servicios',  label: 'Servicios agenda' },
          ]"
          :key="link.to"
          :to="link.to"
          class="bg-white/5 border border-white/[0.07] px-4 py-3 text-[11px] font-bold tracking-wide hover:border-[#f5d984]/40 hover:text-[#f5d984] transition-colors"
        >
          {{ link.label }}
        </RouterLink>
      </div>
    </div>
  </div>
</template>
