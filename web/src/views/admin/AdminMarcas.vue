<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Plus, Pencil, Trash2, Check, X } from 'lucide-vue-next'
import { apiFetch, apiFetchAuth } from '../../lib/api'
import { useAuth } from '../../composables/auth'

const { getAccessToken } = useAuth()

type Marca = { id: number; nombre: string; slug: string }

const cargando  = ref(false)
const errorMsg  = ref('')
const items     = ref<Marca[]>([])
const editId    = ref<number | null>(null)
const editForm  = ref({ nombre: '', slug: '' })
const newForm   = ref({ nombre: '', slug: '' })
const guardando = ref(false)
const creando   = ref(false)

async function cargar() {
  cargando.value = true; errorMsg.value = ''
  try { items.value = await apiFetch<Marca[]>('/catalogo/marcas/') }
  catch (e) { errorMsg.value = e instanceof Error ? e.message : 'Error' }
  finally { cargando.value = false }
}

function iniciarEditar(m: Marca) { editId.value = m.id; editForm.value = { nombre: m.nombre, slug: m.slug } }
function cancelarEditar() { editId.value = null }

async function guardarEditar(m: Marca) {
  const token = getAccessToken(); if (!token) return
  guardando.value = true; errorMsg.value = ''
  try {
    const u = await apiFetchAuth<Marca>(`/catalogo/admin/marcas/${m.id}/`, token, { method: 'PATCH', body: JSON.stringify(editForm.value) })
    items.value = items.value.map(x => x.id === u.id ? u : x)
    editId.value = null
  } catch (e) { errorMsg.value = e instanceof Error ? e.message : 'Error' }
  finally { guardando.value = false }
}

async function eliminar(m: Marca) {
  const token = getAccessToken(); if (!token) return
  if (!confirm(`¿Eliminar "${m.nombre}"?`)) return
  errorMsg.value = ''
  try {
    await apiFetchAuth<void>(`/catalogo/admin/marcas/${m.id}/`, token, { method: 'DELETE' })
    items.value = items.value.filter(x => x.id !== m.id)
  } catch (e) { errorMsg.value = e instanceof Error ? e.message : 'Error' }
}

async function crear() {
  const token = getAccessToken(); if (!token) return
  if (!newForm.value.nombre.trim()) return
  creando.value = true; errorMsg.value = ''
  try {
    const m = await apiFetchAuth<Marca>('/catalogo/admin/marcas/', token, { method: 'POST', body: JSON.stringify(newForm.value) })
    items.value = [...items.value, m]
    newForm.value = { nombre: '', slug: '' }
  } catch (e) { errorMsg.value = e instanceof Error ? e.message : 'Error' }
  finally { creando.value = false }
}

onMounted(cargar)
</script>

<template>
  <div class="p-6 lg:p-10 max-w-2xl">
    <div class="mb-8">
      <p class="text-[10px] tracking-[0.35em] uppercase text-[#f5d984]/70 mb-1">Catálogo</p>
      <h2 class="text-2xl font-black uppercase tracking-tight" style="font-family:'Playfair Display',serif;">Marcas</h2>
    </div>

    <div v-if="errorMsg" class="mb-4 border border-red-500/30 bg-red-500/10 px-4 py-3 text-[11px] text-red-200">{{ errorMsg }}</div>
    <div v-if="cargando" class="py-10 text-center text-[11px] text-white/40">Cargando…</div>

    <div v-else class="bg-white/5 border border-white/[0.07] rounded mb-6 overflow-hidden">
      <table class="w-full text-sm">
        <thead>
          <tr class="border-b border-white/[0.07]">
            <th class="admin-th">Nombre</th>
            <th class="admin-th">Slug</th>
            <th class="admin-th w-20"></th>
          </tr>
        </thead>
        <tbody class="divide-y divide-white/[0.05]">
          <tr v-for="m in items" :key="m.id" class="hover:bg-white/[0.03] transition-colors">
            <td class="px-4 py-3">
              <input v-if="editId === m.id" v-model="editForm.nombre" class="admin-input" />
              <span v-else class="font-semibold">{{ m.nombre }}</span>
            </td>
            <td class="px-4 py-3">
              <input v-if="editId === m.id" v-model="editForm.slug" class="admin-input" />
              <span v-else class="text-white/40 text-[12px]">/{{ m.slug }}</span>
            </td>
            <td class="px-4 py-3">
              <div class="flex items-center gap-1">
                <template v-if="editId === m.id">
                  <button @click="guardarEditar(m)" :disabled="guardando" class="p-1.5 text-[#f5d984] hover:bg-white/10 rounded"><Check class="h-3.5 w-3.5" /></button>
                  <button @click="cancelarEditar" class="p-1.5 text-white/40 hover:bg-white/10 rounded"><X class="h-3.5 w-3.5" /></button>
                </template>
                <template v-else>
                  <button @click="iniciarEditar(m)" class="p-1.5 text-white/40 hover:text-[#f5d984] transition"><Pencil class="h-3.5 w-3.5" /></button>
                  <button @click="eliminar(m)" class="p-1.5 text-white/40 hover:text-red-300 transition"><Trash2 class="h-3.5 w-3.5" /></button>
                </template>
              </div>
            </td>
          </tr>
          <tr v-if="!items.length">
            <td colspan="3" class="px-4 py-8 text-center text-[11px] text-white/30">Sin marcas.</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="bg-white/5 border border-white/[0.07] rounded p-5">
      <p class="text-[10px] font-black tracking-widest uppercase text-white/40 mb-4">Nueva marca</p>
      <div class="flex gap-3 flex-wrap">
        <div class="flex-1 min-w-[140px]">
          <label class="admin-label">Nombre *</label>
          <input v-model="newForm.nombre" type="text" class="admin-input" placeholder="Ray-Ban" />
        </div>
        <div class="flex-1 min-w-[140px]">
          <label class="admin-label">Slug</label>
          <input v-model="newForm.slug" type="text" class="admin-input" placeholder="ray-ban" />
        </div>
        <div class="flex items-end">
          <button @click="crear" :disabled="creando || !newForm.nombre.trim()"
            class="flex items-center gap-2 text-[11px] font-bold tracking-widest uppercase bg-[#f5d984] text-[#314037] px-4 py-2.5 hover:opacity-90 transition disabled:opacity-40">
            <Plus class="h-4 w-4" /> Crear
          </button>
        </div>
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
