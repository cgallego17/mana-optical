<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Plus, Pencil, Trash2, Check, X } from 'lucide-vue-next'
import { apiFetch, apiFetchAuth } from '../../lib/api'
import { useAuth } from '../../composables/auth'
import ServicioHorarioEditor from './ServicioHorarioEditor.vue'
import ServicioExcepcionesEditor from './ServicioExcepcionesEditor.vue'

const { getAccessToken } = useAuth()

type HorarioDia = { inicio: string; fin: string }
type Servicio = {
  id: number; nombre: string; slug: string; duracion_minutos: number
  dias_disponibles: number[]; horarios_dias: Record<string, HorarioDia>
  vigencia_desde: string | null; vigencia_hasta: string | null
}
type ServicioForm = {
  nombre: string; slug: string; duracion_minutos: number
  dias_disponibles: number[]; horarios_dias: Record<string, HorarioDia>
  vigencia_desde: string; vigencia_hasta: string
}

const DIAS = ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom']

function formVacio(): ServicioForm {
  return { nombre: '', slug: '', duracion_minutos: 30, dias_disponibles: [], horarios_dias: {}, vigencia_desde: '', vigencia_hasta: '' }
}

const cargando  = ref(false)
const errorMsg  = ref('')
const items     = ref<Servicio[]>([])
const editId    = ref<number | null>(null)
const editForm  = ref<ServicioForm>(formVacio())
const newForm   = ref<ServicioForm>(formVacio())
const guardando = ref(false)
const creando   = ref(false)

function resumenDias(s: Servicio): string {
  const tieneRestriccion = s.dias_disponibles.length > 0
  const dias = tieneRestriccion ? [...s.dias_disponibles].sort() : [0, 1, 2, 3, 4, 5, 6]
  const horarios = s.horarios_dias ?? {}
  if (!tieneRestriccion && !Object.keys(horarios).length) return 'Todos los días · horario general'
  return dias.map(d => {
    const h = horarios[String(d)]
    return h ? `${DIAS[d]} ${h.inicio}–${h.fin}` : DIAS[d]
  }).join(' · ')
}

function resumenVigencia(s: Servicio): string {
  if (!s.vigencia_desde && !s.vigencia_hasta) return ''
  return `Vigente: ${s.vigencia_desde ?? '…'} → ${s.vigencia_hasta ?? '…'}`
}

function payloadHorario(form: ServicioForm) {
  const horarios_dias: Record<string, HorarioDia> = {}
  for (const [dia, h] of Object.entries(form.horarios_dias)) {
    if (h.inicio && h.fin) horarios_dias[dia] = { inicio: h.inicio, fin: h.fin }
  }
  return {
    horarios_dias,
    vigencia_desde: form.vigencia_desde || null,
    vigencia_hasta: form.vigencia_hasta || null,
  }
}

async function cargar() {
  cargando.value = true; errorMsg.value = ''
  try { items.value = await apiFetch<Servicio[]>('/agenda/servicios/') }
  catch (e) { errorMsg.value = e instanceof Error ? e.message : 'Error' }
  finally { cargando.value = false }
}

function iniciarEditar(s: Servicio) {
  editId.value = s.id
  editForm.value = {
    nombre: s.nombre, slug: s.slug, duracion_minutos: s.duracion_minutos,
    dias_disponibles: [...(s.dias_disponibles ?? [])],
    horarios_dias: Object.fromEntries(Object.entries(s.horarios_dias ?? {}).map(([k, v]) => [k, { ...v }])),
    vigencia_desde: s.vigencia_desde ?? '', vigencia_hasta: s.vigencia_hasta ?? '',
  }
}
function cancelarEditar() { editId.value = null }

async function guardarEditar(s: Servicio) {
  const token = getAccessToken(); if (!token) return
  guardando.value = true; errorMsg.value = ''
  try {
    const body = { ...editForm.value, ...payloadHorario(editForm.value) }
    const u = await apiFetchAuth<Servicio>(`/agenda/admin/servicios/${s.id}/`, token, { method: 'PATCH', body: JSON.stringify(body) })
    items.value = items.value.map(x => x.id === u.id ? u : x)
    editId.value = null
  } catch (e) { errorMsg.value = e instanceof Error ? e.message : 'Error' }
  finally { guardando.value = false }
}

async function eliminar(s: Servicio) {
  const token = getAccessToken(); if (!token) return
  if (!confirm(`¿Eliminar "${s.nombre}"?`)) return
  errorMsg.value = ''
  try {
    await apiFetchAuth<void>(`/agenda/admin/servicios/${s.id}/`, token, { method: 'DELETE' })
    items.value = items.value.filter(x => x.id !== s.id)
  } catch (e) { errorMsg.value = e instanceof Error ? e.message : 'Error' }
}

async function crear() {
  const token = getAccessToken(); if (!token) return
  if (!newForm.value.nombre.trim()) return
  creando.value = true; errorMsg.value = ''
  try {
    const body = { ...newForm.value, ...payloadHorario(newForm.value) }
    const s = await apiFetchAuth<Servicio>('/agenda/admin/servicios/', token, { method: 'POST', body: JSON.stringify(body) })
    items.value = [...items.value, s]
    newForm.value = formVacio()
  } catch (e) { errorMsg.value = e instanceof Error ? e.message : 'Error' }
  finally { creando.value = false }
}

onMounted(cargar)
</script>

<template>
  <div class="p-6 lg:p-10">
    <div class="mb-8">
      <p class="text-[10px] tracking-[0.35em] uppercase text-[#f5d984]/70 mb-1">Agenda</p>
      <h2 class="text-2xl font-black uppercase tracking-tight" style="font-family:'Playfair Display',serif;">Servicios</h2>
      <p class="text-white/40 text-[12px] mt-1">Cada día puede tener su propio horario. Si lo dejas vacío, usa el horario general de la óptica.</p>
    </div>

    <div v-if="errorMsg" class="mb-4 border border-red-500/30 bg-red-500/10 px-4 py-3 text-[11px] text-red-200">{{ errorMsg }}</div>
    <div v-if="cargando" class="py-10 text-center text-[11px] text-white/40">Cargando…</div>

    <div v-else class="bg-white/5 border border-white/[0.07] rounded mb-8 overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full text-sm min-w-[760px]">
          <thead>
            <tr class="border-b border-white/[0.07]">
              <th class="admin-th">Nombre</th>
              <th class="admin-th">Slug</th>
              <th class="admin-th">Duración</th>
              <th class="admin-th">Programación</th>
              <th class="admin-th w-20"></th>
            </tr>
          </thead>
          <tbody class="divide-y divide-white/[0.05]">
            <template v-for="s in items" :key="s.id">
              <tr class="hover:bg-white/[0.03] transition-colors">
                <td class="px-4 py-4 align-top">
                  <input v-if="editId === s.id" v-model="editForm.nombre" class="admin-input" />
                  <span v-else class="font-semibold">{{ s.nombre }}</span>
                </td>
                <td class="px-4 py-4 align-top">
                  <input v-if="editId === s.id" v-model="editForm.slug" class="admin-input" />
                  <span v-else class="text-white/40 text-[12px]">/{{ s.slug }}</span>
                </td>
                <td class="px-4 py-4 align-top">
                  <input v-if="editId === s.id" v-model.number="editForm.duracion_minutos" type="number" min="5" step="5" class="admin-input w-20" />
                  <span v-else class="text-white/60 text-[12px] whitespace-nowrap">{{ s.duracion_minutos }} min</span>
                </td>
                <td class="px-4 py-4 align-top">
                  <ServicioHorarioEditor v-if="editId === s.id" :form="editForm" class="min-w-[360px]" />
                  <div v-else class="text-[11px] text-white/40 space-y-1 max-w-sm">
                    <div>{{ resumenDias(s) }}</div>
                    <div v-if="resumenVigencia(s)" class="text-[#f5d984]/70">{{ resumenVigencia(s) }}</div>
                  </div>
                </td>
                <td class="px-4 py-4 align-top">
                  <div class="flex items-center gap-1">
                    <template v-if="editId === s.id">
                      <button @click="guardarEditar(s)" :disabled="guardando" class="p-1.5 text-[#f5d984] hover:bg-white/10 rounded"><Check class="h-3.5 w-3.5" /></button>
                      <button @click="cancelarEditar" class="p-1.5 text-white/40 hover:bg-white/10 rounded"><X class="h-3.5 w-3.5" /></button>
                    </template>
                    <template v-else>
                      <button @click="iniciarEditar(s)" class="p-1.5 text-white/40 hover:text-[#f5d984] transition"><Pencil class="h-3.5 w-3.5" /></button>
                      <button @click="eliminar(s)" class="p-1.5 text-white/40 hover:text-red-300 transition"><Trash2 class="h-3.5 w-3.5" /></button>
                    </template>
                  </div>
                </td>
              </tr>
              <tr v-if="editId === s.id">
                <td colspan="5" class="px-4 pb-5 pt-1 bg-black/10">
                  <ServicioExcepcionesEditor :servicio-id="s.id" />
                </td>
              </tr>
            </template>
            <tr v-if="!items.length">
              <td colspan="5" class="px-4 py-8 text-center text-[11px] text-white/30">Sin servicios.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div class="bg-white/5 border border-white/[0.07] rounded p-6">
      <p class="text-[10px] font-black tracking-widest uppercase text-white/40 mb-5">Nuevo servicio</p>

      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        <div>
          <label class="admin-label">Nombre *</label>
          <input v-model="newForm.nombre" type="text" class="admin-input" placeholder="Examen Visual" />
        </div>
        <div>
          <label class="admin-label">Slug</label>
          <input v-model="newForm.slug" type="text" class="admin-input" placeholder="examen-visual" />
        </div>
        <div>
          <label class="admin-label">Duración (min)</label>
          <input v-model.number="newForm.duracion_minutos" type="number" min="5" step="5" class="admin-input" />
        </div>
      </div>

      <div class="mt-5 pt-5 border-t border-white/[0.07]">
        <ServicioHorarioEditor :form="newForm" />
      </div>

      <div class="flex justify-end mt-6 pt-5 border-t border-white/[0.07]">
        <button @click="crear" :disabled="creando || !newForm.nombre.trim()"
          class="flex items-center gap-2 text-[11px] font-bold tracking-widest uppercase bg-[#f5d984] text-[#314037] px-5 py-2.5 hover:opacity-90 transition disabled:opacity-40">
          <Plus class="h-4 w-4" /> Crear
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
@reference "../../style.css";
.admin-label { @apply block text-[10px] tracking-widest uppercase text-white/50 mb-1.5 }
.admin-input { @apply w-full px-3 py-2 bg-black/30 border border-white/10 outline-none focus:border-[#f5d984] text-sm text-white rounded }
.admin-th    { @apply px-4 py-3 text-left text-[10px] font-black tracking-widest uppercase text-white/30 }
</style>
