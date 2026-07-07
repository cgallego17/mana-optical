<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Check } from 'lucide-vue-next'
import { apiFetchAuth } from '../../lib/api'
import { useAuth } from '../../composables/auth'

const { getAccessToken } = useAuth()

type Horario = { id: number; dia_semana: number; abierto: boolean; hora_inicio: string; hora_fin: string }

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

onMounted(cargar)
</script>

<template>
  <div class="p-6 lg:p-10 max-w-2xl">
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
  </div>
</template>

<style scoped>
@reference "../../style.css";
.admin-input { @apply w-full px-3 py-2 bg-black/30 border border-white/10 outline-none focus:border-[#f5d984] text-sm text-white rounded }
.admin-th    { @apply px-4 py-3 text-left text-[10px] font-black tracking-widest uppercase text-white/30 }
</style>
