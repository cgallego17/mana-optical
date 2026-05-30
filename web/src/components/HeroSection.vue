<script setup lang="ts">
import { ChevronRight, ChevronLeft, ArrowDown } from 'lucide-vue-next'
import { useAgendaModal } from '../composables/agendaModal'

const { open: openAgenda } = useAgendaModal()
</script>

<template>
  <section class="w-full bg-white overflow-hidden">
    <div class="grid h-screen grid-cols-1 lg:grid-cols-2 overflow-hidden">

      <!-- Left Panel -->
      <div class="relative overflow-hidden flex items-center justify-center min-h-[400px]">
        <img
          src="https://images.unsplash.com/photo-1511499767150-a48a237f0083?auto=format&fit=crop&w=900&q=80"
          alt="Gafas de diseñador"
          class="absolute inset-0 h-full w-full object-cover scale-105 transition-transform duration-[8s] hover:scale-100"
        />
        <div class="absolute inset-0 bg-black/10" />

        <!-- Left arrow -->
        <button class="absolute left-5 top-1/2 -translate-y-1/2 z-20 h-11 w-11 flex items-center justify-center bg-white/80 backdrop-blur-sm hover:bg-white transition-all duration-300 shadow-lg">
          <ChevronLeft class="h-5 w-5 text-black" />
        </button>

        <!-- Eye-chart card -->
        <div class="relative z-10 bg-white/95 backdrop-blur-sm px-12 py-14 text-center shadow-2xl animate-float">
          <div class="font-black text-black leading-none mb-8" style="font-family: 'Playfair Display', serif;">
            <div class="text-7xl mb-2" style="letter-spacing: -0.02em;">T</div>
            <div class="text-5xl mb-2" style="letter-spacing: 0.15em;">EYE</div>
            <div class="text-3xl mb-2" style="letter-spacing: 0.3em;">VISION</div>
            <div class="text-2xl" style="letter-spacing: 0.45em;">CHECK</div>
          </div>
          <div class="w-8 h-px bg-[#f5d984] mx-auto mb-6" />
          <button @click="openAgenda()" class="text-[11px] font-bold uppercase tracking-[0.25em] text-black hover:text-[#f5d984] transition-colors duration-300">
            Reservar cita
          </button>
        </div>

        <!-- Scroll hint -->
        <div class="absolute bottom-6 left-1/2 -translate-x-1/2 z-20 flex flex-col items-center gap-2 animate-bounce opacity-60">
          <ArrowDown class="h-4 w-4 text-black" />
        </div>
      </div>

      <!-- Right Panel -->
      <div class="relative overflow-hidden flex flex-col items-center justify-center min-h-[400px]">
        <img
          src="https://images.unsplash.com/photo-1577803645773-f96470509666?auto=format&fit=crop&w=900&q=80"
          alt="Mujer con gafas"
          class="absolute inset-0 h-full w-full object-cover scale-105 transition-transform duration-[8s] hover:scale-100"
        />
        <div class="absolute inset-0 bg-gradient-to-t from-black/70 via-black/20 to-transparent" />


        <!-- Center text -->
        <div class="relative z-10 text-center px-10">
          <span class="inline-block text-[11px] tracking-[0.4em] uppercase text-[#f5d984] font-medium mb-4">Nueva Colección</span>
          <h2 class="text-5xl lg:text-6xl font-bold text-white mb-4 leading-tight" style="font-family: 'Playfair Display', serif;">
            Una Variedad<br /><em>de Estilos</em>
          </h2>
          <p class="text-sm text-white/70 mb-10 tracking-wide">
            Encuentra la combinación perfecta para ti
          </p>
          <button class="btn-shine active:scale-95 inline-flex items-center gap-3 bg-[#314037] text-white text-[11px] font-bold tracking-[0.25em] uppercase px-10 py-4 hover:bg-[#f5d984] hover:text-[#314037] transition-all duration-300">
            Ver Más <ChevronRight class="h-3.5 w-3.5" />
          </button>
        </div>

        <!-- Carousel dots -->
        <div class="absolute bottom-6 left-1/2 -translate-x-1/2 z-20 flex items-center gap-2">
          <button class="h-1.5 w-8 bg-white rounded-full" />
          <button class="h-1.5 w-1.5 bg-white/40 rounded-full" />
          <button class="h-1.5 w-1.5 bg-white/40 rounded-full" />
        </div>

        <!-- Right arrow -->
        <button class="absolute right-5 top-1/2 -translate-y-1/2 z-20 h-11 w-11 flex items-center justify-center bg-white/20 backdrop-blur-sm hover:bg-white/40 transition-all duration-300">
          <ChevronRight class="h-5 w-5 text-white" />
        </button>
      </div>

    </div>
  </section>
</template>
