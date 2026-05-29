<script setup lang="ts">
import { Truck, ShieldCheck, Headphones } from 'lucide-vue-next'

const services = [
  { icon: Truck, title: 'Envío Gratis', description: 'Entregamos tus gafas a domicilio sin costo adicional en pedidos desde $150.' },
  { icon: ShieldCheck, title: 'Compra Segura', description: 'Pagos protegidos con cifrado SSL. Tu información siempre está segura con nosotros.' },
  { icon: Headphones, title: 'Atención 24/7', description: 'Nuestro equipo de especialistas está disponible para ayudarte en todo momento.' },
]
</script>

<template>
  <section class="w-full bg-[#314037] py-16">
    <div class="grid grid-cols-1 sm:grid-cols-3 max-w-5xl mx-auto">
      <div
        v-for="(service, index) in services"
        :key="service.title"
        v-scroll-reveal="{ delay: index * 200 }"
        class="flex flex-col sm:flex-row items-center sm:items-start gap-5 px-10 py-10 text-center sm:text-left border-black"
        :class="{ 'border-x border-white/10': index === 1 }"
      >
        <div class="flex-shrink-0 h-12 w-12 rounded-full border border-[#f5d984]/50 flex items-center justify-center">
          <component :is="service.icon" class="h-5 w-5 text-[#f5d984]" :stroke-width="1.5" />
        </div>
        <div>
          <h3 class="text-xs font-black tracking-widest uppercase text-white mb-1.5">{{ service.title }}</h3>
          <p class="text-xs text-white/40 leading-relaxed">{{ service.description }}</p>
        </div>
      </div>
    </div>
  </section>
</template>
