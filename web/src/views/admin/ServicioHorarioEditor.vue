<script setup lang="ts">
const DIAS = ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom']

type HorarioDia = { inicio: string; fin: string }
type Form = {
  dias_disponibles: number[]
  horarios_dias: Record<string, HorarioDia>
  vigencia_desde: string
  vigencia_hasta: string
}

const props = defineProps<{ form: Form }>()

function activo(dia: number): boolean {
  return props.form.dias_disponibles.includes(dia)
}

function alternarDia(dia: number) {
  const dias = props.form.dias_disponibles
  const i = dias.indexOf(dia)
  if (i === -1) dias.push(dia)
  else {
    dias.splice(i, 1)
    delete props.form.horarios_dias[String(dia)]
  }
}

function horarioDe(dia: number): HorarioDia {
  const key = String(dia)
  if (!props.form.horarios_dias[key]) props.form.horarios_dias[key] = { inicio: '', fin: '' }
  return props.form.horarios_dias[key]
}
</script>

<template>
  <div>
    <div class="flex items-center justify-between mb-2 gap-4 flex-wrap">
      <label class="admin-label mb-0">Días y horario</label>
      <p class="text-[10px] text-white/30">Deja vacío el horario de un día activo para usar el horario general.</p>
    </div>

    <div class="space-y-1.5">
      <div
        v-for="(d, idx) in DIAS" :key="idx"
        class="flex items-center gap-2 px-2.5 py-1.5 rounded border transition-colors"
        :class="activo(idx) ? 'border-white/10 bg-white/[0.03]' : 'border-white/[0.06]'"
      >
        <button
          type="button" @click="alternarDia(idx)"
          class="w-9 h-7 shrink-0 text-[10px] font-bold rounded border transition-colors"
          :class="activo(idx)
            ? 'bg-[#f5d984] text-[#314037] border-[#f5d984]'
            : 'border-white/15 text-white/40 hover:border-white/30'"
        >{{ d }}</button>

        <template v-if="activo(idx)">
          <input type="time" v-model="horarioDe(idx).inicio" class="admin-input w-[6.5rem] py-1" />
          <span class="text-white/30 text-[11px]">–</span>
          <input type="time" v-model="horarioDe(idx).fin" class="admin-input w-[6.5rem] py-1" />
          <span class="text-[10px] text-white/25 ml-1 whitespace-nowrap">
            {{ horarioDe(idx).inicio && horarioDe(idx).fin ? '' : 'horario general' }}
          </span>
        </template>
        <span v-else class="text-[11px] text-white/25">No disponible</span>
      </div>
    </div>

    <div class="grid grid-cols-2 gap-3 mt-4">
      <div>
        <label class="admin-label">Vigente desde</label>
        <input type="date" v-model="form.vigencia_desde" class="admin-input" />
      </div>
      <div>
        <label class="admin-label">Vigente hasta</label>
        <input type="date" v-model="form.vigencia_hasta" class="admin-input" />
      </div>
    </div>
  </div>
</template>

<style scoped>
@reference "../../style.css";
.admin-label { @apply block text-[10px] tracking-widest uppercase text-white/50 mb-1.5 }
.admin-input { @apply w-full px-3 py-2 bg-black/30 border border-white/10 outline-none focus:border-[#f5d984] text-sm text-white rounded }
</style>
