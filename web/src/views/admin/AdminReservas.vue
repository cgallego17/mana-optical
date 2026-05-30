<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { Check, X, RefreshCw } from 'lucide-vue-next'
import { apiFetchAuth } from '../../lib/api'
import { useAuth } from '../../composables/auth'

const { getAccessToken } = useAuth()

type Reserva = {
  id: number
  nombre: string
  telefono: string
  fecha: string
  hora: string
  servicio_nombre: string
  estado: 'pendiente' | 'confirmada' | 'cancelada'
  creada_en?: string
}

const cargando  = ref(false)
const errorMsg  = ref('')
const reservas  = ref<Reserva[]>([])
const filtro    = ref<'todas' | 'pendiente' | 'confirmada' | 'cancelada'>('todas')
const actualizando = ref<number | null>(null)

const reservasFiltradas = computed(() =>
  filtro.value === 'todas' ? reservas.value : reservas.value.filter(r => r.estado === filtro.value)
)

async function cargar() {
  const token = getAccessToken(); if (!token) return
  cargando.value = true; errorMsg.value = ''
  try {
    const data = await apiFetchAuth<Reserva[] | { results: Reserva[] }>('/agenda/admin/reservas/', token)
    reservas.value = (Array.isArray(data) ? data : data.results)
      .sort((a, b) => new Date(b.fecha + 'T' + b.hora).getTime() - new Date(a.fecha + 'T' + a.hora).getTime())
  } catch (e) { errorMsg.value = e instanceof Error ? e.message : 'Error cargando reservas' }
  finally { cargando.value = false }
}

async function cambiarEstado(r: Reserva, estado: Reserva['estado']) {
  const token = getAccessToken(); if (!token) return
  actualizando.value = r.id
  try {
    const u = await apiFetchAuth<Reserva>(`/agenda/admin/reservas/${r.id}/`, token, { method: 'PATCH', body: JSON.stringify({ estado }) })
    reservas.value = reservas.value.map(x => x.id === u.id ? u : x)
  } catch (e) { errorMsg.value = e instanceof Error ? e.message : 'Error actualizando'
  } finally { actualizando.value = null }
}

function formatFecha(fecha: string, hora: string) {
  try {
    const d = new Date(`${fecha}T${hora}`)
    return d.toLocaleDateString('es-CO', { weekday: 'short', day: 'numeric', month: 'short' }) + ' · ' + hora
  } catch { return `${fecha} ${hora}` }
}

const estadoBadge: Record<string, string> = {
  pendiente:  'bg-amber-500/20 text-amber-300',
  confirmada: 'bg-emerald-500/20 text-emerald-300',
  cancelada:  'bg-red-500/20 text-red-300',
}

const filtros: { value: typeof filtro.value; label: string }[] = [
  { value: 'todas',     label: 'Todas' },
  { value: 'pendiente', label: 'Pendientes' },
  { value: 'confirmada',label: 'Confirmadas' },
  { value: 'cancelada', label: 'Canceladas' },
]

onMounted(cargar)
</script>

<template>
  <div class="p-6 lg:p-10">
    <div class="flex items-center justify-between mb-8 flex-wrap gap-4">
      <div>
        <p class="text-[10px] tracking-[0.35em] uppercase text-[#f5d984]/70 mb-1">Agenda</p>
        <h2 class="text-2xl font-black uppercase tracking-tight" style="font-family:'Playfair Display',serif;">Reservas</h2>
      </div>
      <button @click="cargar" :disabled="cargando"
        class="flex items-center gap-2 text-[11px] font-bold tracking-widest uppercase border border-white/20 px-4 py-2 hover:border-white/50 transition disabled:opacity-40">
        <RefreshCw class="h-3.5 w-3.5" :class="cargando ? 'animate-spin' : ''" /> Actualizar
      </button>
    </div>

    <!-- Filtros de estado -->
    <div class="flex gap-2 flex-wrap mb-6">
      <button
        v-for="f in filtros" :key="f.value"
        @click="filtro = f.value"
        class="text-[11px] font-bold tracking-widest uppercase px-4 py-2 rounded transition"
        :class="filtro === f.value ? 'bg-[#f5d984] text-[#314037]' : 'bg-white/5 text-white/50 hover:text-white hover:bg-white/10'"
      >{{ f.label }}</button>
    </div>

    <div v-if="errorMsg" class="mb-5 border border-red-500/30 bg-red-500/10 px-4 py-3 text-[11px] text-red-200">{{ errorMsg }}</div>
    <div v-if="cargando" class="py-16 text-center text-[11px] text-white/40">Cargando reservas…</div>

    <!-- Tabla -->
    <div v-else class="bg-white/5 border border-white/[0.07] rounded overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead>
            <tr class="border-b border-white/[0.07]">
              <th class="admin-th">Fecha y hora</th>
              <th class="admin-th">Servicio</th>
              <th class="admin-th">Cliente</th>
              <th class="admin-th hidden sm:table-cell">Teléfono</th>
              <th class="admin-th">Estado</th>
              <th class="admin-th w-24">Acciones</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-white/[0.05]">
            <tr v-for="r in reservasFiltradas" :key="r.id" class="hover:bg-white/[0.03] transition-colors">
              <td class="px-4 py-3 text-[12px]">{{ formatFecha(r.fecha, r.hora) }}</td>
              <td class="px-4 py-3 font-semibold text-[12px]">{{ r.servicio_nombre }}</td>
              <td class="px-4 py-3 text-[12px]">{{ r.nombre }}</td>
              <td class="px-4 py-3 hidden sm:table-cell text-white/50 text-[12px]">
                <a :href="`https://wa.me/57${r.telefono.replace(/\D/g,'')}`" target="_blank" class="hover:text-[#25D366] transition">
                  {{ r.telefono }}
                </a>
              </td>
              <td class="px-4 py-3">
                <span class="text-[9px] font-bold tracking-widest uppercase px-2 py-0.5 rounded"
                  :class="estadoBadge[r.estado] || 'bg-white/10 text-white/40'">
                  {{ r.estado }}
                </span>
              </td>
              <td class="px-4 py-3">
                <div class="flex items-center gap-1">
                  <button
                    v-if="r.estado !== 'confirmada'"
                    @click="cambiarEstado(r, 'confirmada')"
                    :disabled="actualizando === r.id"
                    class="p-1.5 text-white/40 hover:text-emerald-300 transition disabled:opacity-40"
                    title="Confirmar"
                  ><Check class="h-3.5 w-3.5" /></button>
                  <button
                    v-if="r.estado !== 'cancelada'"
                    @click="cambiarEstado(r, 'cancelada')"
                    :disabled="actualizando === r.id"
                    class="p-1.5 text-white/40 hover:text-red-300 transition disabled:opacity-40"
                    title="Cancelar"
                  ><X class="h-3.5 w-3.5" /></button>
                </div>
              </td>
            </tr>
            <tr v-if="!reservasFiltradas.length">
              <td colspan="6" class="px-4 py-12 text-center text-[11px] text-white/30">No hay reservas.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<style scoped>
@reference "../../style.css";
.admin-th { @apply px-4 py-3 text-left text-[10px] font-black tracking-widest uppercase text-white/30 }
</style>
