<script setup lang="ts">
import { ref, watch } from 'vue'
import { Plus, Trash2 } from 'lucide-vue-next'
import { apiFetchAuth } from '../../lib/api'
import { useAuth } from '../../composables/auth'

const props = defineProps<{ servicioId: number }>()
const { getAccessToken } = useAuth()

type ExcepcionApi = {
  id: number; servicio: number; fecha: string; abierto: boolean
  hora_inicio: string | null; hora_fin: string | null; motivo: string
}

const items    = ref<ExcepcionApi[]>([])
const cargando = ref(false)
const errorMsg = ref('')
const guardando = ref(false)
const eliminando = ref<number | null>(null)

const nuevaFecha = ref('')
const nuevoAbierto = ref(false)
const nuevaHoraInicio = ref('09:00')
const nuevaHoraFin = ref('18:00')
const nuevoMotivo = ref('')

async function cargar() {
  const token = getAccessToken(); if (!token) return
  cargando.value = true; errorMsg.value = ''
  try {
    items.value = await apiFetchAuth<ExcepcionApi[]>(`/agenda/admin/servicios/excepciones/?servicio=${props.servicioId}`, token)
  } catch (e) { errorMsg.value = e instanceof Error ? e.message : 'Error' }
  finally { cargando.value = false }
}

async function agregar() {
  const token = getAccessToken(); if (!token || !nuevaFecha.value) return
  guardando.value = true; errorMsg.value = ''
  try {
    const body: Record<string, unknown> = {
      servicio: props.servicioId, fecha: nuevaFecha.value, abierto: nuevoAbierto.value, motivo: nuevoMotivo.value,
    }
    if (nuevoAbierto.value) { body.hora_inicio = nuevaHoraInicio.value; body.hora_fin = nuevaHoraFin.value }
    const creada = await apiFetchAuth<ExcepcionApi>('/agenda/admin/servicios/excepciones/', token, { method: 'POST', body: JSON.stringify(body) })
    items.value = [...items.value, creada].sort((a, b) => a.fecha.localeCompare(b.fecha))
    nuevaFecha.value = ''; nuevoMotivo.value = ''; nuevoAbierto.value = false
  } catch (e) { errorMsg.value = e instanceof Error ? e.message : 'Error creando la fecha especial' }
  finally { guardando.value = false }
}

async function eliminar(e: ExcepcionApi) {
  const token = getAccessToken(); if (!token) return
  eliminando.value = e.id; errorMsg.value = ''
  try {
    await apiFetchAuth(`/agenda/admin/servicios/excepciones/${e.id}/`, token, { method: 'DELETE' })
    items.value = items.value.filter(x => x.id !== e.id)
  } catch (err) { errorMsg.value = err instanceof Error ? err.message : 'Error eliminando' }
  finally { eliminando.value = null }
}

function formatFecha(fecha: string) {
  const d = new Date(fecha + 'T00:00:00')
  return d.toLocaleDateString('es-CO', { weekday: 'short', day: 'numeric', month: 'short', year: 'numeric' })
}

watch(() => props.servicioId, cargar, { immediate: true })
</script>

<template>
  <div>
    <p class="text-[10px] font-black tracking-widest uppercase text-white/40 mb-1">Fechas especiales de este servicio</p>
    <p class="text-[10px] text-white/30 mb-3">Cierra un día puntual (festivo, ausencia del especialista) o habilita una apertura extra fuera de su horario habitual. Tiene prioridad sobre el resto de reglas.</p>

    <div v-if="errorMsg" class="mb-3 border border-red-500/30 bg-red-500/10 px-3 py-2 text-[11px] text-red-200">{{ errorMsg }}</div>

    <div class="flex flex-wrap items-end gap-3 mb-4">
      <div>
        <label class="admin-label">Fecha</label>
        <input v-model="nuevaFecha" type="date" class="admin-input w-36" />
      </div>
      <div>
        <label class="admin-label">Tipo</label>
        <div class="flex bg-black/30 border border-white/10 rounded overflow-hidden">
          <button type="button" @click="nuevoAbierto = false"
            class="px-2.5 py-2 text-[10px] font-bold uppercase tracking-wide"
            :class="!nuevoAbierto ? 'bg-[#f5d984] text-[#314037]' : 'text-white/50'">Cerrado</button>
          <button type="button" @click="nuevoAbierto = true"
            class="px-2.5 py-2 text-[10px] font-bold uppercase tracking-wide"
            :class="nuevoAbierto ? 'bg-[#f5d984] text-[#314037]' : 'text-white/50'">Apertura extra</button>
        </div>
      </div>
      <template v-if="nuevoAbierto">
        <div>
          <label class="admin-label">Desde</label>
          <input v-model="nuevaHoraInicio" type="time" class="admin-input w-24" />
        </div>
        <div>
          <label class="admin-label">Hasta</label>
          <input v-model="nuevaHoraFin" type="time" class="admin-input w-24" />
        </div>
      </template>
      <div class="flex-1 min-w-[140px]">
        <label class="admin-label">Motivo</label>
        <input v-model="nuevoMotivo" type="text" placeholder="Festivo, vacaciones..." class="admin-input" />
      </div>
      <button
        type="button" @click="agregar" :disabled="!nuevaFecha || guardando"
        class="flex items-center gap-1.5 text-[10px] font-bold tracking-widest uppercase bg-[#f5d984] text-[#314037] px-3 py-2 rounded disabled:opacity-40"
      >
        <Plus class="h-3 w-3" /> Agregar
      </button>
    </div>

    <div v-if="cargando" class="text-[11px] text-white/30">Cargando…</div>
    <ul v-else-if="items.length" class="space-y-1.5">
      <li v-for="e in items" :key="e.id" class="flex items-center gap-3 text-[11px] px-3 py-2 bg-black/20 rounded border border-white/[0.06]">
        <span class="font-semibold text-white/70 whitespace-nowrap">{{ formatFecha(e.fecha) }}</span>
        <span class="text-[9px] font-bold tracking-widest uppercase px-2 py-0.5 rounded shrink-0"
          :class="e.abierto ? 'bg-emerald-500/20 text-emerald-300' : 'bg-red-500/20 text-red-300'">
          {{ e.abierto ? 'Apertura extra' : 'Cerrado' }}
        </span>
        <span class="text-white/50 whitespace-nowrap">{{ e.abierto ? `${e.hora_inicio}–${e.hora_fin}` : '—' }}</span>
        <span class="text-white/40 truncate flex-1">{{ e.motivo || '—' }}</span>
        <button @click="eliminar(e)" :disabled="eliminando === e.id" class="p-1 text-white/40 hover:text-red-300 rounded disabled:opacity-40 shrink-0">
          <Trash2 class="h-3.5 w-3.5" />
        </button>
      </li>
    </ul>
    <p v-else class="text-[11px] text-white/25">Sin fechas especiales para este servicio.</p>
  </div>
</template>

<style scoped>
@reference "../../style.css";
.admin-label { @apply block text-[10px] tracking-widest uppercase text-white/50 mb-1.5 }
.admin-input { @apply w-full px-3 py-2 bg-black/30 border border-white/10 outline-none focus:border-[#f5d984] text-sm text-white rounded }
</style>
