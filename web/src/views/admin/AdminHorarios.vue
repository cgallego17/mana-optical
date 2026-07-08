<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Check, Plus, Trash2 } from 'lucide-vue-next'
import { apiFetchAuth } from '../../lib/api'
import { useAuth } from '../../composables/auth'

const { getAccessToken } = useAuth()

type Horario = { id: number; dia_semana: number; abierto: boolean; hora_inicio: string; hora_fin: string }
type Excepcion = { id: number; fecha: string; abierto: boolean; hora_inicio: string | null; hora_fin: string | null; motivo: string }

const NOMBRES_DIA = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']

const cargando = ref(false)
const errorMsg = ref('')
const okMsg    = ref('')
const items    = ref<Horario[]>([])
const guardando = ref<number | null>(null)

async function cargar() {
  const token = getAccessToken(); if (!token) return
  cargando.value = true; errorMsg.value = ''
  try {
    const data = await apiFetchAuth<Horario[]>('/agenda/admin/horarios/', token)
    items.value = [...data].sort((a, b) => a.dia_semana - b.dia_semana)
  } catch (e) { errorMsg.value = e instanceof Error ? e.message : 'Error' }
  finally { cargando.value = false }
}

async function guardar(h: Horario) {
  const token = getAccessToken(); if (!token) return
  guardando.value = h.id; errorMsg.value = ''; okMsg.value = ''
  try {
    const u = await apiFetchAuth<Horario>(`/agenda/admin/horarios/${h.id}/`, token, {
      method: 'PATCH',
      body: JSON.stringify({ abierto: h.abierto, hora_inicio: h.hora_inicio, hora_fin: h.hora_fin }),
    })
    items.value = items.value.map(x => x.id === u.id ? u : x)
    okMsg.value = `Horario de ${NOMBRES_DIA[u.dia_semana]} actualizado.`
  } catch (e) { errorMsg.value = e instanceof Error ? e.message : 'Error' }
  finally { guardando.value = null }
}

// Fechas especiales (excepciones): festivos/cierres puntuales o aperturas extra
const excepciones = ref<Excepcion[]>([])
const cargandoExc = ref(false)
const errorExc = ref('')
const guardandoExc = ref(false)
const eliminando = ref<number | null>(null)

const nuevaFecha = ref('')
const nuevoAbierto = ref(false)
const nuevaHoraInicio = ref('09:00')
const nuevaHoraFin = ref('18:00')
const nuevoMotivo = ref('')

async function cargarExcepciones() {
  const token = getAccessToken(); if (!token) return
  cargandoExc.value = true; errorExc.value = ''
  try {
    const data = await apiFetchAuth<Excepcion[]>('/agenda/admin/excepciones/', token)
    excepciones.value = [...data].sort((a, b) => a.fecha.localeCompare(b.fecha))
  } catch (e) { errorExc.value = e instanceof Error ? e.message : 'Error' }
  finally { cargandoExc.value = false }
}

async function agregarExcepcion() {
  const token = getAccessToken(); if (!token || !nuevaFecha.value) return
  guardandoExc.value = true; errorExc.value = ''
  try {
    const body: Record<string, unknown> = {
      fecha: nuevaFecha.value,
      abierto: nuevoAbierto.value,
      motivo: nuevoMotivo.value,
    }
    if (nuevoAbierto.value) {
      body.hora_inicio = nuevaHoraInicio.value
      body.hora_fin = nuevaHoraFin.value
    }
    const creada = await apiFetchAuth<Excepcion>('/agenda/admin/excepciones/', token, {
      method: 'POST',
      body: JSON.stringify(body),
    })
    excepciones.value = [...excepciones.value, creada].sort((a, b) => a.fecha.localeCompare(b.fecha))
    nuevaFecha.value = ''; nuevoMotivo.value = ''; nuevoAbierto.value = false
  } catch (e) { errorExc.value = e instanceof Error ? e.message : 'Error creando la fecha especial' }
  finally { guardandoExc.value = false }
}

async function eliminarExcepcion(e: Excepcion) {
  const token = getAccessToken(); if (!token) return
  eliminando.value = e.id; errorExc.value = ''
  try {
    await apiFetchAuth(`/agenda/admin/excepciones/${e.id}/`, token, { method: 'DELETE' })
    excepciones.value = excepciones.value.filter(x => x.id !== e.id)
  } catch (err) { errorExc.value = err instanceof Error ? err.message : 'Error eliminando' }
  finally { eliminando.value = null }
}

function formatFechaExc(fecha: string) {
  const d = new Date(fecha + 'T00:00:00')
  return d.toLocaleDateString('es-CO', { weekday: 'short', day: 'numeric', month: 'short', year: 'numeric' })
}

onMounted(() => { cargar(); cargarExcepciones() })
</script>

<template>
  <div class="p-6 lg:p-10 max-w-3xl">
    <div class="mb-8">
      <p class="text-[10px] tracking-[0.35em] uppercase text-[#f5d984]/70 mb-1">Agenda</p>
      <h2 class="text-2xl font-black uppercase tracking-tight" style="font-family:'Playfair Display',serif;">Horarios</h2>
      <p class="text-white/40 text-[12px] mt-1">Define los días laborales y el horario de atención para agendar citas.</p>
    </div>

    <div v-if="errorMsg" class="mb-4 border border-red-500/30 bg-red-500/10 px-4 py-3 text-[11px] text-red-200">{{ errorMsg }}</div>
    <div v-if="okMsg" class="mb-4 border border-emerald-500/30 bg-emerald-500/10 px-4 py-3 text-[11px] text-emerald-200">{{ okMsg }}</div>
    <div v-if="cargando" class="py-10 text-center text-[11px] text-white/40">Cargando…</div>

    <div v-else class="bg-white/5 border border-white/[0.07] rounded overflow-hidden">
      <table class="w-full text-sm">
        <thead>
          <tr class="border-b border-white/[0.07]">
            <th class="admin-th">Día</th>
            <th class="admin-th w-24">Abierto</th>
            <th class="admin-th">Desde</th>
            <th class="admin-th">Hasta</th>
            <th class="admin-th w-16"></th>
          </tr>
        </thead>
        <tbody class="divide-y divide-white/[0.05]">
          <tr v-for="h in items" :key="h.id" class="hover:bg-white/[0.03] transition-colors">
            <td class="px-4 py-3 font-semibold">{{ NOMBRES_DIA[h.dia_semana] }}</td>
            <td class="px-4 py-3">
              <button
                type="button" @click="h.abierto = !h.abierto"
                class="w-11 h-6 rounded-full transition-colors relative"
                :class="h.abierto ? 'bg-[#f5d984]' : 'bg-white/15'"
              >
                <span class="absolute top-0.5 h-5 w-5 bg-[#0f1612] rounded-full transition-transform"
                  :class="h.abierto ? 'translate-x-[22px]' : 'translate-x-0.5'" />
              </button>
            </td>
            <td class="px-4 py-3">
              <input v-model="h.hora_inicio" type="time" :disabled="!h.abierto" class="admin-input w-28 disabled:opacity-30" />
            </td>
            <td class="px-4 py-3">
              <input v-model="h.hora_fin" type="time" :disabled="!h.abierto" class="admin-input w-28 disabled:opacity-30" />
            </td>
            <td class="px-4 py-3">
              <button @click="guardar(h)" :disabled="guardando === h.id" class="p-1.5 text-[#f5d984] hover:bg-white/10 rounded disabled:opacity-40">
                <Check class="h-3.5 w-3.5" />
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Fechas especiales -->
    <div class="mt-12">
      <div class="mb-5">
        <h3 class="text-lg font-black uppercase tracking-tight" style="font-family:'Playfair Display',serif;">Fechas especiales</h3>
        <p class="text-white/40 text-[12px] mt-1">Cierra un día puntual (festivo, vacaciones) o habilita una apertura extra fuera del horario semanal.</p>
      </div>

      <div v-if="errorExc" class="mb-4 border border-red-500/30 bg-red-500/10 px-4 py-3 text-[11px] text-red-200">{{ errorExc }}</div>

      <!-- Formulario nueva excepción -->
      <div class="bg-white/5 border border-white/[0.07] rounded p-4 mb-6 flex flex-wrap items-end gap-4">
        <div>
          <label class="block text-[10px] font-black tracking-widest uppercase text-white/40 mb-1.5">Fecha</label>
          <input v-model="nuevaFecha" type="date" class="admin-input w-40" />
        </div>
        <div>
          <label class="block text-[10px] font-black tracking-widest uppercase text-white/40 mb-1.5">Tipo</label>
          <div class="flex bg-black/30 border border-white/10 rounded overflow-hidden">
            <button type="button" @click="nuevoAbierto = false"
              class="px-3 py-2 text-[11px] font-bold uppercase tracking-wide"
              :class="!nuevoAbierto ? 'bg-[#f5d984] text-[#314037]' : 'text-white/50'">Cerrado</button>
            <button type="button" @click="nuevoAbierto = true"
              class="px-3 py-2 text-[11px] font-bold uppercase tracking-wide"
              :class="nuevoAbierto ? 'bg-[#f5d984] text-[#314037]' : 'text-white/50'">Apertura extra</button>
          </div>
        </div>
        <template v-if="nuevoAbierto">
          <div>
            <label class="block text-[10px] font-black tracking-widest uppercase text-white/40 mb-1.5">Desde</label>
            <input v-model="nuevaHoraInicio" type="time" class="admin-input w-28" />
          </div>
          <div>
            <label class="block text-[10px] font-black tracking-widest uppercase text-white/40 mb-1.5">Hasta</label>
            <input v-model="nuevaHoraFin" type="time" class="admin-input w-28" />
          </div>
        </template>
        <div class="flex-1 min-w-[160px]">
          <label class="block text-[10px] font-black tracking-widest uppercase text-white/40 mb-1.5">Motivo (opcional)</label>
          <input v-model="nuevoMotivo" type="text" placeholder="Festivo, vacaciones..." class="admin-input" />
        </div>
        <button
          @click="agregarExcepcion"
          :disabled="!nuevaFecha || guardandoExc"
          class="flex items-center gap-2 text-[11px] font-bold tracking-widest uppercase bg-[#f5d984] text-[#314037] px-4 py-2.5 rounded disabled:opacity-40"
        >
          <Plus class="h-3.5 w-3.5" /> Agregar
        </button>
      </div>

      <div v-if="cargandoExc" class="py-6 text-center text-[11px] text-white/40">Cargando…</div>
      <div v-else class="bg-white/5 border border-white/[0.07] rounded overflow-hidden">
        <table class="w-full text-sm">
          <thead>
            <tr class="border-b border-white/[0.07]">
              <th class="admin-th">Fecha</th>
              <th class="admin-th">Tipo</th>
              <th class="admin-th">Horario</th>
              <th class="admin-th">Motivo</th>
              <th class="admin-th w-16"></th>
            </tr>
          </thead>
          <tbody class="divide-y divide-white/[0.05]">
            <tr v-for="e in excepciones" :key="e.id" class="hover:bg-white/[0.03] transition-colors">
              <td class="px-4 py-3 font-semibold">{{ formatFechaExc(e.fecha) }}</td>
              <td class="px-4 py-3">
                <span class="text-[9px] font-bold tracking-widest uppercase px-2 py-0.5 rounded"
                  :class="e.abierto ? 'bg-emerald-500/20 text-emerald-300' : 'bg-red-500/20 text-red-300'">
                  {{ e.abierto ? 'Apertura extra' : 'Cerrado' }}
                </span>
              </td>
              <td class="px-4 py-3 text-white/60">{{ e.abierto ? `${e.hora_inicio} - ${e.hora_fin}` : '—' }}</td>
              <td class="px-4 py-3 text-white/50">{{ e.motivo || '—' }}</td>
              <td class="px-4 py-3">
                <button @click="eliminarExcepcion(e)" :disabled="eliminando === e.id" class="p-1.5 text-white/40 hover:text-red-300 rounded disabled:opacity-40">
                  <Trash2 class="h-3.5 w-3.5" />
                </button>
              </td>
            </tr>
            <tr v-if="!excepciones.length">
              <td colspan="5" class="px-4 py-8 text-center text-[11px] text-white/30">No hay fechas especiales configuradas.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<style scoped>
@reference "../../style.css";
.admin-input { @apply w-full px-3 py-2 bg-black/30 border border-white/10 outline-none focus:border-[#f5d984] text-sm text-white rounded }
.admin-th    { @apply px-4 py-3 text-left text-[10px] font-black tracking-widest uppercase text-white/30 }
</style>
