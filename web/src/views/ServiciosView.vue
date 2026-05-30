<script setup lang="ts">
import ServicesSection from '../components/ServicesSection.vue'
</script>

<template>
  <div class="pt-[108px]">
    <section class="bg-[#314037] py-16 px-8 text-center">
      <p class="text-[11px] tracking-[0.4em] uppercase text-[#f5d984] mb-3">Lo que hacemos</p>
      <h1 class="text-4xl lg:text-5xl font-black text-white uppercase tracking-tight mb-3" style="font-family:'Playfair Display',serif;">
        Servicios
      </h1>
      <p class="text-white/60 text-sm max-w-2xl mx-auto text-center">Exámenes visuales, monturas premium, lentes oftálmicos y más. Calidad clínica con estética de lujo.</p>
    </section>

    <section class="bg-white">
      <ServicesSection />
    </section>

    <section class="bg-[#f8f7f5] py-16 px-8 text-center">
      <RouterLink
        to="/agenda"
        class="btn-shine inline-flex items-center gap-3 bg-[#f5d984] text-[#314037] text-[11px] font-bold tracking-[0.25em] uppercase px-10 py-4 hover:opacity-90 transition-opacity"
      >
        Reserva tu cita ahora
      </RouterLink>
    </section>
  </div>
</template>
