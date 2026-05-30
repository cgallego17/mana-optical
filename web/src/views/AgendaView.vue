<script setup lang="ts">
import BookingSection from '../components/BookingSection.vue'
import { useAgendaModal } from '../composables/agendaModal'

const { open: openAgenda } = useAgendaModal()
</script>

<template>
  <div class="pt-[108px]">
    <section class="bg-[#314037] py-16 px-8 text-center">
      <p class="text-[11px] tracking-[0.4em] uppercase text-[#f5d984] mb-3">Agenda Digital</p>
      <h1 class="text-4xl lg:text-5xl font-black text-white uppercase tracking-tight mb-3" style="font-family:'Playfair Display',serif;">
        Reserva tu Cita
      </h1>
      <div class="flex justify-center px-4">
        <p class="text-white/60 text-sm text-center max-w-sm">Selecciona el tipo de servicio y el horario disponible. Confirmación inmediata por WhatsApp.</p>
      </div>
    </section>

    <section class="bg-white">
      <BookingSection />
    </section>

    <section class="bg-[#314037] py-16 px-8 text-center">
      <p class="text-white/70 text-sm mb-4">¿Dudas o necesitas ayuda?</p>
      <button
        @click="openAgenda()"
        class="btn-shine inline-flex items-center gap-3 bg-[#f5d984] text-[#314037] text-[11px] font-bold tracking-[0.25em] uppercase px-10 py-4 hover:opacity-90 transition-opacity"
      >
        Reservar Cita
      </button>
    </section>
  </div>
</template>
