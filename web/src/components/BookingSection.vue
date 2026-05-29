<script setup lang="ts">
import { CheckCircle2, XCircle, ArrowRight } from 'lucide-vue-next'

const services = [
  {
    image: 'https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?auto=format&fit=crop&w=700&q=80',
    tag: 'Salud Visual',
    title: 'Examen Visual Completo',
    features: [
      { text: 'Evaluación de agudeza visual y refracción', ok: true },
      { text: 'Revisión de presión intraocular', ok: true },
      { text: 'Diagnóstico de enfermedades oculares', ok: false },
    ],
  },
  {
    image: 'https://images.unsplash.com/photo-1617471346061-5d329ab9c574?auto=format&fit=crop&w=700&q=80',
    tag: 'Online',
    title: 'Agenda tu Examen',
    features: [
      { text: 'Reserva desde cualquier dispositivo', ok: true },
      { text: 'Confirmación inmediata por correo', ok: true },
      { text: 'Recordatorio automático de tu cita', ok: true },
    ],
  },
  {
    image: 'https://images.unsplash.com/photo-1551190822-a9333d879b1f?auto=format&fit=crop&w=700&q=80',
    tag: 'Premium',
    title: 'Tratamientos Médicos',
    features: [
      { text: 'Especialistas certificados', ok: true },
      { text: 'Tecnología de diagnóstico avanzada', ok: true },
      { text: 'Seguimiento personalizado', ok: false },
    ],
  },
]
</script>

<template>
  <section class="w-full bg-white py-24 px-8 lg:px-16">

    <!-- Header -->
    <div v-scroll-reveal class="mb-16 flex flex-col items-center text-center">
      <span class="inline-block text-[11px] tracking-[0.35em] uppercase text-[#f5d984] font-medium mb-4">Servicios</span>
      <h2 class="text-4xl lg:text-5xl font-black tracking-tight text-black uppercase mb-4">
        Agenda una Cita
      </h2>
      <p class="text-sm text-black/40">Reserva tu turno con nuestros especialistas de forma rápida y sencilla</p>
    </div>

    <!-- Cards -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-6xl mx-auto">
      <div
        v-for="(service, i) in services"
        :key="service.title"
        v-scroll-reveal="{ delay: i * 180 }"
        class="group border border-black/8 hover:border-black/20 hover:shadow-xl transition-all duration-500 flex flex-col overflow-hidden"
      >
        <!-- Image -->
        <div class="relative overflow-hidden h-52">
          <img :src="service.image" :alt="service.title"
            class="h-full w-full object-cover transition-transform duration-700 group-hover:scale-105" />
          <div class="absolute inset-0 bg-gradient-to-t from-black/40 to-transparent" />
          <span class="absolute top-4 left-4 bg-[#f5d984] text-[#314037] text-[10px] font-bold tracking-widest uppercase px-3 py-1">
            {{ service.tag }}
          </span>
        </div>

        <div class="p-7 flex flex-col flex-1">
          <h3 class="text-sm font-black tracking-wide uppercase text-black mb-5">{{ service.title }}</h3>

          <ul class="space-y-3 mb-8 flex-1">
            <li v-for="feature in service.features" :key="feature.text" class="flex items-start gap-3">
              <CheckCircle2 v-if="feature.ok" class="h-4 w-4 text-black flex-shrink-0 mt-0.5" :stroke-width="1.5" />
              <XCircle v-else class="h-4 w-4 text-black/20 flex-shrink-0 mt-0.5" :stroke-width="1.5" />
              <span class="text-xs leading-relaxed" :class="feature.ok ? 'text-black/60' : 'text-black/25'">{{ feature.text }}</span>
            </li>
          </ul>

          <button class="btn-shine active:scale-95 w-full flex items-center justify-center gap-2 bg-[#314037] text-white text-[11px] font-bold tracking-[0.25em] uppercase py-4 hover:bg-[#f5d984] hover:text-[#314037] transition-colors duration-300">
            Reservar Cita <ArrowRight class="h-3.5 w-3.5" />
          </button>
        </div>
      </div>
    </div>

  </section>
</template>
