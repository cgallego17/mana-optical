<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { Check, X, RefreshCw, Plus } from 'lucide-vue-next'
import { apiFetchAuth, unwrapResults, ApiError } from '../../lib/api'
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

type ServicioApi = { id: number; nombre: string }

const cargando  = ref(false)
const errorMsg  = ref('')
const reservas  = ref<Reserva[]>([])
const filtro    = ref<'todas' | 'pendiente' | 'confirmada' | 'cancelada'>('todas')
const actualizando = ref<number | null>(null)

// Nueva cita manual (creada directamente por el admin)
const servicios = ref<ServicioApi[]>([])
const mostrarForm = ref(false)
const creando = ref(false)
const errorForm = ref('')
const nueva = ref({
  servicio: '' as number | '',
  fecha: '',
  hora: '',
  nombre: '',
  telefono: '',
  email: '',
  notas: '',
  estado: 'confirmada' as Reserva['estado'],
})

async function cargarServicios() {
  const token = getAccessToken(); if (!token) return
  try {
    const data = await apiFetchAuth<ServicioApi[] | { results: ServicioApi[] }>('/agenda/admin/servicios/', token)
    servicios.value = unwrapResults<ServicioApi>(data)
  } catch { servicios.value = [] }
}

function abrirForm() {
  errorForm.value = ''
  nueva.value = { servicio: '', fecha: '', hora: '', nombre: '', telefono: '', email: '', notas: '', estado: 'confirmada' }
  mostrarForm.value = true
}

async function crearCita() {
  const token = getAccessToken(); if (!token) return
  errorForm.value = ''
  if (!nueva.value.fecha || !nueva.value.hora || !nueva.value.nombre.trim() || !nueva.value.telefono.trim()) {
    errorForm.value = 'Fecha, hora, nombre y teléfono son obligatorios.'
    return
  }
  creando.value = true
  try {
    const body: Record<string, unknown> = {
      fecha: nueva.value.fecha,
      hora: nueva.value.hora,
      nombre: nueva.value.nombre.trim(),
      telefono: nueva.value.telefono.trim(),
      email: nueva.value.email.trim(),
      notas: nueva.value.notas.trim(),
      estado: nueva.value.estado,
    }
    if (nueva.value.servicio) body.servicio = nueva.value.servicio
    const creada = await apiFetchAuth<Reserva>('/agenda/admin/reservas/', token, {
      method: 'POST',
      body: JSON.stringify(body),
    })
    reservas.value = [creada, ...reservas.value]
    mostrarForm.value = false
  } catch (e) {
    errorForm.value = e instanceof ApiError ? e.message : (e instanceof Error ? e.message : 'Error creando la cita')
  } finally { creando.value = false }
}

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

onMounted(() => { cargar(); cargarServicios() })
</script>

<template>
  <div class="p-6 lg:p-10">
    <div class="flex items-center justify-between mb-8 flex-wrap gap-4">
      <div>
        <p class="text-[10px] tracking-[0.35em] uppercase text-[#f5d984]/70 mb-1">Agenda</p>
        <h2 class="text-2xl font-black uppercase tracking-tight" style="font-family:'Playfair Display',serif;">Reservas</h2>
      </div>
      <div class="flex items-center gap-3">
        <button @click="abrirForm"
          class="flex items-center gap-2 text-[11px] font-bold tracking-widest uppercase bg-[#f5d984] text-[#314037] px-4 py-2 rounded hover:opacity-90 transition">
          <Plus class="h-3.5 w-3.5" /> Nueva cita
        </button>
        <button @click="cargar" :disabled="cargando"
          class="flex items-center gap-2 text-[11px] font-bold tracking-widest uppercase border border-white/20 px-4 py-2 hover:border-white/50 transition disabled:opacity-40">
          <RefreshCw class="h-3.5 w-3.5" :class="cargando ? 'animate-spin' : ''" /> Actualizar
        </button>
      </div>
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

    <!-- Modal: nueva cita manual -->
    <div v-if="mostrarForm" class="fixed inset-0 z-[95] flex items-center justify-center p-4">
      <div class="absolute inset-0 bg-black/60" @click="mostrarForm = false" />
      <div class="relative bg-[#1a231f] border border-white/10 w-full max-w-md p-6 rounded shadow-2xl">
        <h3 class="text-base font-black uppercase tracking-wide mb-5">Nueva cita</h3>

        <div v-if="errorForm" class="mb-4 border border-red-500/30 bg-red-500/10 px-4 py-3 text-[11px] text-red-200">{{ errorForm }}</div>

        <div class="space-y-4">
          <div>
            <label class="block text-[10px] font-black tracking-widest uppercase text-white/40 mb-1.5">Servicio</label>
            <select v-model="nueva.servicio" class="admin-input">
              <option value="">Sin especificar</option>
              <option v-for="s in servicios" :key="s.id" :value="s.id">{{ s.nombre }}</option>
            </select>
          </div>
          <div class="flex gap-3">
            <div class="flex-1">
              <label class="block text-[10px] font-black tracking-widest uppercase text-white/40 mb-1.5">Fecha *</label>
              <input v-model="nueva.fecha" type="date" class="admin-input" />
            </div>
            <div class="flex-1">
              <label class="block text-[10px] font-black tracking-widest uppercase text-white/40 mb-1.5">Hora *</label>
              <input v-model="nueva.hora" type="time" class="admin-input" />
            </div>
          </div>
          <div>
            <label class="block text-[10px] font-black tracking-widest uppercase text-white/40 mb-1.5">Nombre *</label>
            <input v-model="nueva.nombre" type="text" class="admin-input" placeholder="Nombre del cliente" />
          </div>
          <div class="flex gap-3">
            <div class="flex-1">
              <label class="block text-[10px] font-black tracking-widest uppercase text-white/40 mb-1.5">Teléfono *</label>
              <input v-model="nueva.telefono" type="tel" class="admin-input" placeholder="300 000 0000" />
            </div>
            <div class="flex-1">
              <label class="block text-[10px] font-black tracking-widest uppercase text-white/40 mb-1.5">Email</label>
              <input v-model="nueva.email" type="email" class="admin-input" />
            </div>
          </div>
          <div>
            <label class="block text-[10px] font-black tracking-widest uppercase text-white/40 mb-1.5">Estado</label>
            <select v-model="nueva.estado" class="admin-input">
              <option value="confirmada">Confirmada</option>
              <option value="pendiente">Pendiente</option>
            </select>
          </div>
          <div>
            <label class="block text-[10px] font-black tracking-widest uppercase text-white/40 mb-1.5">Notas</label>
            <textarea v-model="nueva.notas" rows="2" class="admin-input resize-none" />
          </div>
        </div>

        <div class="flex items-center justify-end gap-3 mt-6">
          <button @click="mostrarForm = false" class="text-[11px] font-bold tracking-widest uppercase text-white/50 hover:text-white px-4 py-2.5 transition">Cancelar</button>
          <button @click="crearCita" :disabled="creando"
            class="text-[11px] font-bold tracking-widest uppercase bg-[#f5d984] text-[#314037] px-5 py-2.5 rounded disabled:opacity-40">
            {{ creando ? 'Creando…' : 'Crear cita' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
@reference "../../style.css";
.admin-th { @apply px-4 py-3 text-left text-[10px] font-black tracking-widest uppercase text-white/30 }
.admin-input { @apply w-full px-3 py-2 bg-black/30 border border-white/10 outline-none focus:border-[#f5d984] text-sm text-white rounded }
</style>
