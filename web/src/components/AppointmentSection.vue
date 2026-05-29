<script setup lang="ts">
import bgImage from '../assets/hero.png'
import { ArrowRight } from 'lucide-vue-next'
</script>

<template>
  <section
    class="relative w-full flex items-center justify-center py-24 px-6"
    :style="{
      backgroundImage: `url('${bgImage}')`,
      backgroundAttachment: 'fixed',
      backgroundSize: 'cover',
      backgroundPosition: 'center',
      minHeight: '500px',
    }"
  >
    <div class="absolute inset-0 bg-black/65" />

    <div v-scroll-reveal class="relative z-10 w-full max-w-xl flex flex-col items-center text-center">
      <span class="inline-block text-[11px] tracking-[0.4em] uppercase text-[#f5d984] font-medium mb-4">Contacto Directo</span>
      <h2 class="text-3xl lg:text-4xl font-black tracking-tight uppercase text-white mb-3">
        Reserva tu Cita
      </h2>
      <div class="w-12 h-px bg-[#f5d984] mx-auto mb-6" />
      <p class="text-sm text-white/60 mb-10 leading-relaxed text-center">
        Escríbenos por WhatsApp y te atendemos de inmediato.<br/>Estamos para ayudarte — Betania, Antioquia.
      </p>

      <div class="flex shadow-2xl">
        <input
          type="text"
          placeholder="Escribe tu consulta o mensaje..."
          class="flex-1 bg-white px-6 py-5 text-sm text-black placeholder:text-black/35 outline-none"
        />
        <button class="btn-shine active:scale-95 bg-[#314037] text-white px-8 py-5 text-[11px] font-bold tracking-[0.25em] uppercase hover:bg-[#f5d984] hover:text-[#314037] transition-all duration-300 flex-shrink-0 flex items-center gap-2">
          Enviar <ArrowRight class="h-3.5 w-3.5" />
        </button>
      </div>
    </div>
  </section>
</template>
