<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Plus, Pencil, Trash2, Check, X } from 'lucide-vue-next'
import { apiFetch, apiFetchAuth } from '../../lib/api'
import { useAuth } from '../../composables/auth'

const { getAccessToken } = useAuth()

type Servicio = {
  id: number; nombre: string; slug: string; duracion_minutos: number
  dias_disponibles: number[]; hora_inicio: string | null; hora_fin: string | null
}

const DIAS = ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom']

const cargando  = ref(false)
const errorMsg  = ref('')
const items     = ref<Servicio[]>([])
const editId    = ref<number | null>(null)
const editForm  = ref({ nombre: '', slug: '', duracion_minutos: 30, dias_disponibles: [] as number[], hora_inicio: '', hora_fin: '' })
const newForm   = ref({ nombre: '', slug: '', duracion_minutos: 30, dias_disponibles: [] as number[], hora_inicio: '', hora_fin: '' })
const guardando = ref(false)
const creando   = ref(false)

function alternarDia(dias: number[], d: number) {
  const i = dias.indexOf(d)
  if (i === -1) dias.push(d)
  else dias.splice(i, 1)
}

function textoDias(dias: number[]): string {
  if (!dias.length) return 'Todos los días'
  return [...dias].sort().map(d => DIAS[d]).join(', ')
}

function textoHoras(s: Servicio): string {
  return s.hora_inicio && s.hora_fin ? `${s.hora_inicio}–${s.hora_fin}` : 'Horario general'
}

function payloadHoras(form: { hora_inicio: string; hora_fin: string }) {
  return {
    hora_inicio: form.hora_inicio || null,
    hora_fin: form.hora_fin || null,
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
    hora_inicio: s.hora_inicio ?? '', hora_fin: s.hora_fin ?? '',
  }
}
function cancelarEditar() { editId.value = null }

async function guardarEditar(s: Servicio) {
  const token = getAccessToken(); if (!token) return
  guardando.value = true; errorMsg.value = ''
  try {
    const body = { ...editForm.value, ...payloadHoras(editForm.value) }
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
    const body = { ...newForm.value, ...payloadHoras(newForm.value) }
    const s = await apiFetchAuth<Servicio>('/agenda/admin/servicios/', token, { method: 'POST', body: JSON.stringify(body) })
    items.value = [...items.value, s]
    newForm.value = { nombre: '', slug: '', duracion_minutos: 30, dias_disponibles: [], hora_inicio: '', hora_fin: '' }
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
      <p class="text-white/40 text-[12px] mt-1">Si no defines un horario propio, el servicio usa el horario general de la óptica.</p>
    </div>

    <div v-if="errorMsg" class="mb-4 border border-red-500/30 bg-red-500/10 px-4 py-3 text-[11px] text-red-200">{{ errorMsg }}</div>
    <div v-if="cargando" class="py-10 text-center text-[11px] text-white/40">Cargando…</div>

    <div v-else class="bg-white/5 border border-white/[0.07] rounded mb-8 overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full text-sm min-w-[820px]">
          <thead>
            <tr class="border-b border-white/[0.07]">
              <th class="admin-th">Nombre</th>
              <th class="admin-th">Slug</th>
              <th class="admin-th">Duración</th>
              <th class="admin-th w-[220px]">Días</th>
              <th class="admin-th">Horario</th>
              <th class="admin-th w-20"></th>
            </tr>
          </thead>
          <tbody class="divide-y divide-white/[0.05]">
            <tr v-for="s in items" :key="s.id" class="hover:bg-white/[0.03] transition-colors">
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
                <div v-if="editId === s.id" class="flex gap-1.5 flex-wrap max-w-[200px]">
                  <button
                    v-for="(d, idx) in DIAS" :key="idx" type="button"
                    @click="alternarDia(editForm.dias_disponibles, idx)"
                    class="w-8 h-7 text-[10px] font-bold rounded border transition-colors"
                    :class="editForm.dias_disponibles.includes(idx)
                      ? 'bg-[#f5d984] text-[#314037] border-[#f5d984]'
                      : 'border-white/15 text-white/40 hover:border-white/30'"
                  >{{ d }}</button>
                </div>
                <span v-else class="text-white/40 text-[11px]">{{ textoDias(s.dias_disponibles) }}</span>
              </td>
              <td class="px-4 py-4 align-top">
                <div v-if="editId === s.id" class="flex items-center gap-1.5">
                  <input v-model="editForm.hora_inicio" type="time" class="admin-input w-24" />
                  <span class="text-white/30">–</span>
                  <input v-model="editForm.hora_fin" type="time" class="admin-input w-24" />
                </div>
                <span v-else class="text-white/40 text-[11px] whitespace-nowrap">{{ textoHoras(s) }}</span>
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
            <tr v-if="!items.length">
              <td colspan="6" class="px-4 py-8 text-center text-[11px] text-white/30">Sin servicios.</td>
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

      <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mt-5">
        <div>
          <label class="admin-label">Días disponibles</label>
          <div class="flex gap-1.5 flex-wrap">
            <button
              v-for="(d, idx) in DIAS" :key="idx" type="button"
              @click="alternarDia(newForm.dias_disponibles, idx)"
              class="w-9 h-9 text-[10px] font-bold rounded border transition-colors"
              :class="newForm.dias_disponibles.includes(idx)
                ? 'bg-[#f5d984] text-[#314037] border-[#f5d984]'
                : 'border-white/15 text-white/40 hover:border-white/30'"
            >{{ d }}</button>
          </div>
        </div>
        <div>
          <label class="admin-label">Horario propio (opcional)</label>
          <div class="flex items-center gap-2">
            <input v-model="newForm.hora_inicio" type="time" class="admin-input w-28" />
            <span class="text-white/30">–</span>
            <input v-model="newForm.hora_fin" type="time" class="admin-input w-28" />
          </div>
        </div>
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
