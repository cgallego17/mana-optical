<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { X, ChevronLeft, ChevronRight, Check, Calendar, Clock, User, MessageCircle } from 'lucide-vue-next'
import { useAgendaModal } from '../composables/agendaModal'
import { apiFetch, unwrapResults } from '../lib/api'

const { isOpen, close } = useAgendaModal()

// Pasos: 1=servicio 2=fecha 3=hora 4=datos 5=confirmación
const paso = ref(1)
const servicioSeleccionado = ref<number | null>(null)
const fechaSeleccionada = ref<Date | null>(null)
const horaSeleccionada = ref('')
const nombre = ref('')
const telefono = ref('')

type ServicioApi = {
  id: number
  nombre: string
  slug: string
  duracion_minutos: number
  dias_disponibles: number[]
}

type SlotApi = {
  hora: string
  disponible: boolean
}

type HorarioApi = {
  dia_semana: number // 0=Lunes … 6=Domingo
  abierto: boolean
  hora_inicio: string
  hora_fin: string
}

type ExcepcionApi = {
  fecha: string
  abierto: boolean
  hora_inicio: string | null
  hora_fin: string | null
  motivo: string
}

const servicios = ref<ServicioApi[]>([])
const horarios = ref<HorarioApi[]>([])
const excepciones = ref<ExcepcionApi[]>([])
const slots = ref<SlotApi[]>([])
const cargandoServicios = ref(false)
const cargandoSlots = ref(false)
const creandoReserva = ref(false)
const errorMsg = ref('')

async function cargarHorarios() {
  try {
    horarios.value = await apiFetch<HorarioApi[]>('/agenda/horarios/')
  } catch {
    horarios.value = []
  }
}

async function cargarExcepciones() {
  try {
    excepciones.value = await apiFetch<ExcepcionApi[]>('/agenda/excepciones/')
  } catch {
    excepciones.value = []
  }
}

function horarioDelDia(diaPy: number): HorarioApi | undefined {
  return horarios.value.find(h => h.dia_semana === diaPy)
}

function excepcionDeFecha(iso: string): ExcepcionApi | undefined {
  return excepciones.value.find(e => e.fecha === iso)
}

const diasAbiertosTexto = computed(() => {
  if (!horarios.value.length) return 'Atención: Lunes a Sábado · Cerrado domingos'
  const abiertos = horarios.value
    .filter(h => h.abierto)
    .sort((a, b) => a.dia_semana - b.dia_semana)
    .map(h => nombreDias[(h.dia_semana + 1) % 7])
  return abiertos.length ? `Atención: ${abiertos.join(', ')}` : 'Sin días de atención configurados'
})

const servicioActual = computed(() =>
  servicioSeleccionado.value
    ? servicios.value.find(s => s.id === servicioSeleccionado.value) ?? null
    : null
)

// Calendario
const hoy = new Date()
const mesActual = ref(new Date(hoy.getFullYear(), hoy.getMonth(), 1))
const nombreMeses = ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']
const nombreDias = ['Dom','Lun','Mar','Mié','Jue','Vie','Sáb']

const diasDelMes = computed(() => {
  const año = mesActual.value.getFullYear()
  const mes = mesActual.value.getMonth()
  const primero = new Date(año, mes, 1).getDay()
  const total = new Date(año, mes + 1, 0).getDate()
  const dias: (Date | null)[] = Array(primero).fill(null)
  for (let d = 1; d <= total; d++) dias.push(new Date(año, mes, d))
  return dias
})

function esDiaValido(d: Date | null): boolean {
  if (!d) return false
  if (d < new Date(hoy.getFullYear(), hoy.getMonth(), hoy.getDate())) return false
  // Excepción de calendario (festivo/cierre o apertura extra) tiene prioridad
  const excepcion = excepcionDeFecha(formatIsoDate(d))
  if (excepcion) {
    if (!excepcion.abierto) return false
  } else {
    const diaPy = (d.getDay() + 6) % 7 // 0=Lunes … 6=Domingo
    const horario = horarioDelDia(diaPy)
    if (horario && !horario.abierto) return false
  }
  // Restricción de días propia del servicio
  const diaPy = (d.getDay() + 6) % 7
  const diasServicio = servicioActual.value?.dias_disponibles ?? []
  if (!excepcion && diasServicio.length && !diasServicio.includes(diaPy)) return false
  // Solo 30 días adelante
  const limite = new Date(hoy); limite.setDate(hoy.getDate() + 30)
  return d <= limite
}

function esDiaSeleccionado(d: Date | null): boolean {
  if (!d || !fechaSeleccionada.value) return false
  return d.toDateString() === fechaSeleccionada.value.toDateString()
}

function mesAnterior() {
  const m = new Date(mesActual.value)
  m.setMonth(m.getMonth() - 1)
  mesActual.value = m
}
function mesSiguiente() {
  const m = new Date(mesActual.value)
  m.setMonth(m.getMonth() + 1)
  mesActual.value = m
}

const horas = computed(() => slots.value.map(s => s.hora))

function esHoraOcupada(h: string): boolean {
  const slot = slots.value.find(s => s.hora === h)
  return slot ? !slot.disponible : true
}

const formatFecha = (d: Date | null) => {
  if (!d) return ''
  return `${d.getDate()} de ${nombreMeses[d.getMonth()]} de ${d.getFullYear()}`
}

const waLink = computed(() => {
  if (!servicioActual.value || !fechaSeleccionada.value || !horaSeleccionada.value) return '#'
  const servicio = servicioActual.value.nombre
  const fecha = formatFecha(fechaSeleccionada.value)
  const msg = encodeURIComponent(
    `Hola Maná Óptical 👋\n\nQuiero agendar una cita:\n• *Servicio:* ${servicio}\n• *Fecha:* ${fecha}\n• *Hora:* ${horaSeleccionada.value}\n• *Nombre:* ${nombre.value}\n• *Teléfono:* ${telefono.value}\n\n¡Gracias!`
  )
  return `https://wa.me/573005262309?text=${msg}`
})

function formatIsoDate(d: Date): string {
  const y = d.getFullYear()
  const m = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  return `${y}-${m}-${day}`
}

async function cargarServicios() {
  cargandoServicios.value = true
  errorMsg.value = ''
  try {
    const data = await apiFetch<ServicioApi[] | { results: ServicioApi[] }>('/agenda/servicios/')
    servicios.value = unwrapResults<ServicioApi>(data)
  } catch (e) {
    errorMsg.value = e instanceof Error ? e.message : 'Error cargando servicios'
  } finally {
    cargandoServicios.value = false
  }
}

async function cargarSlots() {
  if (!fechaSeleccionada.value) return
  cargandoSlots.value = true
  errorMsg.value = ''
  try {
    const params = new URLSearchParams({ fecha: formatIsoDate(fechaSeleccionada.value) })
    if (servicioSeleccionado.value) params.set('servicio', String(servicioSeleccionado.value))
    const data = await apiFetch<{ fecha: string; slots: SlotApi[] }>(
      `/agenda/disponibilidad/?${params.toString()}`,
    )
    slots.value = data.slots
    if (horaSeleccionada.value && esHoraOcupada(horaSeleccionada.value)) {
      horaSeleccionada.value = ''
    }
  } catch (e) {
    slots.value = []
    errorMsg.value = e instanceof Error ? e.message : 'Error cargando disponibilidad'
  } finally {
    cargandoSlots.value = false
  }
}

async function crearReserva() {
  if (!servicioSeleccionado.value || !fechaSeleccionada.value || !horaSeleccionada.value) return
  creandoReserva.value = true
  errorMsg.value = ''
  try {
    await apiFetch('/agenda/reservas/', {
      method: 'POST',
      body: JSON.stringify({
        servicio: servicioSeleccionado.value,
        fecha: formatIsoDate(fechaSeleccionada.value),
        hora: horaSeleccionada.value,
        nombre: nombre.value,
        telefono: telefono.value,
      }),
    })
    paso.value = 5
  } catch (e) {
    errorMsg.value = e instanceof Error ? e.message : 'Error creando reserva'
  } finally {
    creandoReserva.value = false
  }
}

function reset() {
  paso.value = 1
  servicioSeleccionado.value = null
  fechaSeleccionada.value = null
  horaSeleccionada.value = ''
  nombre.value = ''
  telefono.value = ''
  mesActual.value = new Date(hoy.getFullYear(), hoy.getMonth(), 1)
  servicios.value = []
  slots.value = []
  cargandoServicios.value = false
  cargandoSlots.value = false
  creandoReserva.value = false
  errorMsg.value = ''
}

watch(isOpen, (val) => {
  document.body.style.overflow = val ? 'hidden' : ''
  if (val) {
    cargarServicios()
    cargarHorarios()
    cargarExcepciones()
  } else {
    setTimeout(reset, 300)
  }
})

watch(fechaSeleccionada, async (val) => {
  slots.value = []
  if (!val) return
  await cargarSlots()
})

watch(servicioSeleccionado, () => {
  if (fechaSeleccionada.value && !esDiaValido(fechaSeleccionada.value)) {
    fechaSeleccionada.value = null
    horaSeleccionada.value = ''
  }
})
</script>

<template>
  <transition name="fade">
    <div v-if="isOpen" class="fixed inset-0 z-[95] flex items-center justify-center p-4">
      <!-- Backdrop -->
      <div class="absolute inset-0 bg-black/60 backdrop-blur-sm" @click="close" />

      <!-- Panel -->
      <div class="relative bg-white w-full max-w-xl max-h-[90vh] flex flex-col shadow-2xl overflow-hidden">

        <!-- Header del modal -->
        <div class="bg-[#314037] px-6 py-5 flex items-center justify-between shrink-0">
          <div>
            <p class="text-[9px] tracking-[0.3em] uppercase text-[#f5d984] font-medium mb-0.5">Maná Óptical</p>
            <h2 class="text-base font-black text-white tracking-wide uppercase">Reservar Cita</h2>
          </div>
          <button @click="close" class="p-2 text-white/60 hover:text-white hover:bg-white/10 rounded transition">
            <X class="h-5 w-5" />
          </button>
        </div>

        <!-- Indicador de pasos -->
        <div class="flex border-b border-black/[0.08] shrink-0">
          <div
            v-for="n in 4" :key="n"
            class="flex-1 h-1 transition-colors duration-300"
            :class="paso > n ? 'bg-[#314037]' : paso === n ? 'bg-[#f5d984]' : 'bg-black/10'"
          />
        </div>

        <!-- Contenido -->
        <div class="flex-1 overflow-y-auto p-6">

          <div v-if="errorMsg" class="mb-5 border border-red-200 bg-red-50 px-4 py-3 text-[11px] text-red-700">
            {{ errorMsg }}
          </div>

          <!-- Paso 1: Elegir servicio -->
          <div v-if="paso === 1">
            <div class="flex items-center gap-2 mb-5">
              <Calendar class="h-4 w-4 text-[#314037]" />
              <h3 class="text-sm font-black tracking-wide uppercase">¿Qué servicio necesitas?</h3>
            </div>
            <div class="space-y-3">
              <button
                v-for="s in servicios" :key="s.id"
                @click="servicioSeleccionado = s.id"
                class="w-full text-left p-4 border-2 transition-all duration-200"
                :class="servicioSeleccionado === s.id
                  ? 'border-[#314037] bg-[#314037]/5'
                  : 'border-black/10 hover:border-black/25'"
              >
                <div class="flex items-start justify-between gap-2">
                  <div>
                    <p class="text-sm font-bold text-black mb-1">{{ s.nombre }}</p>
                    <p class="text-xs text-black/45">{{ s.duracion_minutos }} min</p>
                  </div>
                  <div class="flex flex-col items-end gap-2 shrink-0">
                    <span class="text-[10px] font-bold tracking-wide text-[#314037] bg-[#f5d984]/40 px-2 py-0.5">{{ s.duracion_minutos }} min</span>
                    <span v-if="servicioSeleccionado === s.id" class="h-5 w-5 bg-[#314037] flex items-center justify-center rounded-full">
                      <Check class="h-3 w-3 text-white" />
                    </span>
                  </div>
                </div>
              </button>
            </div>
            <p v-if="cargandoServicios" class="text-[10px] text-black/35 mt-4">Cargando servicios...</p>
          </div>

          <!-- Paso 2: Elegir fecha -->
          <div v-if="paso === 2">
            <div class="flex items-center gap-2 mb-5">
              <Calendar class="h-4 w-4 text-[#314037]" />
              <h3 class="text-sm font-black tracking-wide uppercase">Selecciona una fecha</h3>
            </div>

            <!-- Navegación de mes -->
            <div class="flex items-center justify-between mb-4">
              <button @click="mesAnterior" class="p-2 hover:bg-black/5 rounded transition">
                <ChevronLeft class="h-4 w-4" />
              </button>
              <span class="text-sm font-bold">
                {{ nombreMeses[mesActual.getMonth()] }} {{ mesActual.getFullYear() }}
              </span>
              <button @click="mesSiguiente" class="p-2 hover:bg-black/5 rounded transition">
                <ChevronRight class="h-4 w-4" />
              </button>
            </div>

            <!-- Encabezados días -->
            <div class="grid grid-cols-7 mb-1">
              <div v-for="d in nombreDias" :key="d"
                class="text-center text-[9px] font-bold tracking-wider uppercase text-black/35 py-1">
                {{ d }}
              </div>
            </div>

            <!-- Días del mes -->
            <div class="grid grid-cols-7 gap-1">
              <div v-for="(dia, i) in diasDelMes" :key="i" class="aspect-square">
                <button
                  v-if="dia"
                  @click="esDiaValido(dia) && (fechaSeleccionada = dia)"
                  :disabled="!esDiaValido(dia)"
                  class="h-full w-full text-[12px] font-semibold rounded transition-colors"
                  :class="[
                    esDiaSeleccionado(dia)
                      ? 'bg-[#314037] text-[#f5d984] font-black'
                      : esDiaValido(dia)
                        ? 'hover:bg-[#f5d984]/40 text-black'
                        : 'text-black/20 cursor-not-allowed'
                  ]"
                >{{ dia.getDate() }}</button>
              </div>
            </div>
            <p class="text-[10px] text-black/35 mt-4">
              {{ (servicioActual?.dias_disponibles?.length ?? 0) > 0
                ? `Disponible: ${servicioActual!.dias_disponibles.map(d => nombreDias[(d + 1) % 7]).join(', ')}`
                : diasAbiertosTexto }}
            </p>
          </div>

          <!-- Paso 3: Elegir hora -->
          <div v-if="paso === 3">
            <div class="flex items-center gap-2 mb-1">
              <Clock class="h-4 w-4 text-[#314037]" />
              <h3 class="text-sm font-black tracking-wide uppercase">Selecciona la hora</h3>
            </div>
            <p class="text-[11px] text-black/40 mb-5">{{ formatFecha(fechaSeleccionada) }}</p>
            <div class="grid grid-cols-3 sm:grid-cols-4 gap-2">
              <button
                v-for="h in horas" :key="h"
                @click="!esHoraOcupada(h) && (horaSeleccionada = h)"
                :disabled="esHoraOcupada(h)"
                class="py-2.5 text-[12px] font-semibold border-2 transition-all"
                :class="[
                  horaSeleccionada === h
                    ? 'border-[#314037] bg-[#314037] text-[#f5d984] font-black'
                    : esHoraOcupada(h)
                      ? 'border-black/8 text-black/20 cursor-not-allowed bg-black/3'
                      : 'border-black/12 hover:border-[#314037] hover:text-[#314037]'
                ]"
              >{{ h }}</button>
            </div>
            <p v-if="cargandoSlots" class="text-[10px] text-black/35 mt-4">Cargando disponibilidad...</p>
            <p v-else class="text-[10px] text-black/30 mt-4">Los horarios en gris ya están reservados.</p>
          </div>

          <!-- Paso 4: Datos personales -->
          <div v-if="paso === 4">
            <div class="flex items-center gap-2 mb-5">
              <User class="h-4 w-4 text-[#314037]" />
              <h3 class="text-sm font-black tracking-wide uppercase">Tus datos</h3>
            </div>

            <!-- Resumen -->
            <div class="bg-[#f8f7f5] p-4 mb-6 space-y-1 text-[11px] text-black/55">
              <p><span class="font-bold text-black/70">Servicio:</span> {{ servicioActual?.nombre }}</p>
              <p><span class="font-bold text-black/70">Fecha:</span> {{ formatFecha(fechaSeleccionada) }}</p>
              <p><span class="font-bold text-black/70">Hora:</span> {{ horaSeleccionada }}</p>
            </div>

            <div class="space-y-4">
              <div>
                <label class="block text-[10px] font-black tracking-[0.2em] uppercase text-black/40 mb-2">Nombre completo *</label>
                <input
                  v-model="nombre" type="text" placeholder="Tu nombre"
                  class="w-full px-4 py-3 border border-black/15 text-sm outline-none focus:border-[#314037] transition"
                />
              </div>
              <div>
                <label class="block text-[10px] font-black tracking-[0.2em] uppercase text-black/40 mb-2">WhatsApp *</label>
                <input
                  v-model="telefono" type="tel" placeholder="300 000 0000"
                  class="w-full px-4 py-3 border border-black/15 text-sm outline-none focus:border-[#314037] transition"
                />
              </div>
            </div>
          </div>

          <!-- Paso 5: Confirmación -->
          <div v-if="paso === 5" class="text-center py-4">
            <div class="h-16 w-16 bg-[#314037] rounded-full flex items-center justify-center mx-auto mb-5">
              <Check class="h-8 w-8 text-[#f5d984]" />
            </div>
            <h3 class="text-lg font-black uppercase mb-2">¡Cita lista para confirmar!</h3>
            <p class="text-sm text-black/50 mb-6">
              Haz clic en el botón para enviar tu solicitud por WhatsApp.<br>
              Te responderemos en minutos para confirmar.
            </p>
            <div class="bg-[#f8f7f5] p-4 text-left space-y-1.5 text-[11px] text-black/60 mb-6">
              <p><span class="font-bold text-black/80">Nombre:</span> {{ nombre }}</p>
              <p><span class="font-bold text-black/80">Servicio:</span> {{ servicioActual?.nombre }}</p>
              <p><span class="font-bold text-black/80">Fecha:</span> {{ formatFecha(fechaSeleccionada) }}</p>
              <p><span class="font-bold text-black/80">Hora:</span> {{ horaSeleccionada }}</p>
            </div>
            <a
              :href="waLink"
              target="_blank"
              @click="close"
              class="btn-shine w-full flex items-center justify-center gap-3 bg-[#25D366] text-white text-[11px] font-bold tracking-[0.25em] uppercase px-8 py-4 hover:opacity-90 transition-opacity"
            >
              <MessageCircle class="h-4 w-4" /> Confirmar por WhatsApp
            </a>
          </div>

        </div>

        <!-- Footer con botones de navegación -->
        <div class="border-t border-black/[0.08] px-6 py-4 flex items-center justify-between shrink-0 bg-white">
          <button
            v-if="paso > 1"
            @click="paso--"
            class="flex items-center gap-2 text-[11px] font-bold tracking-wide uppercase text-black/50 hover:text-black transition"
          >
            <ChevronLeft class="h-4 w-4" /> Atrás
          </button>
          <div v-else />

          <button
            v-if="paso < 5"
            @click="paso === 4 ? crearReserva() : paso++"
            :disabled="
              (paso === 1 && !servicioSeleccionado) ||
              (paso === 2 && !fechaSeleccionada) ||
              (paso === 3 && !horaSeleccionada) ||
              (paso === 4 && (!nombre.trim() || !telefono.trim() || creandoReserva))
            "
            class="btn-shine flex items-center gap-2 bg-[#314037] text-[#f5d984] text-[11px] font-bold tracking-[0.2em] uppercase px-6 py-3 hover:bg-[#f5d984] hover:text-[#314037] transition-colors duration-300 disabled:opacity-30 disabled:cursor-not-allowed disabled:hover:bg-[#314037] disabled:hover:text-[#f5d984]"
          >
            {{ paso === 4 ? (creandoReserva ? 'Creando...' : 'Confirmar') : 'Continuar' }} <ChevronRight class="h-4 w-4" />
          </button>
        </div>

      </div>
    </div>
  </transition>
</template>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity .2s ease }
.fade-enter-from, .fade-leave-to { opacity: 0 }
</style>
