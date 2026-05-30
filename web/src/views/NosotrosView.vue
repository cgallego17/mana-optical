<script setup lang="ts">
import { Eye, Heart, Shield, Star } from 'lucide-vue-next'
import ParallaxDivider from '../components/ParallaxDivider.vue'

const valores = [
  { icon: Eye,    titulo: 'Visión',      desc: 'Cuidamos tu salud visual con tecnología de punta y profesionales certificados.' },
  { icon: Heart,  titulo: 'Compromiso',  desc: 'Estamos comprometidos con el bienestar de cada persona que nos visita en Betania.' },
  { icon: Shield, titulo: 'Calidad',     desc: 'Trabajamos solo con productos y marcas de la más alta calidad del mercado.' },
  { icon: Star,   titulo: 'Excelencia',  desc: 'Brindamos una atención personalizada y un servicio excepcional en cada visita.' },
]
</script>

<template>
  <div class="pt-[108px]">

    <!-- Hero -->
    <div class="bg-[#314037] py-20 px-8 text-center">
      <p class="text-[11px] tracking-[0.4em] uppercase text-[#f5d984] mb-3">Quiénes Somos</p>
      <h1 class="text-4xl lg:text-5xl font-black text-white uppercase tracking-tight mb-3" style="font-family:'Playfair Display',serif;">
        Maná Óptical
      </h1>
      <div class="flex justify-center px-4">
        <p class="text-white/50 text-sm text-center max-w-sm leading-relaxed">
          Especialistas en salud visual y óptica de diseño en Betania, Antioquia.
        </p>
      </div>
    </div>

    <!-- Historia -->
    <section class="w-full py-24 px-8 lg:px-16 bg-white">
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-16 max-w-6xl mx-auto items-center">
        <div v-scroll-reveal>
          <p class="text-[11px] tracking-[0.4em] uppercase text-[#f5d984] font-medium mb-4">Nuestra Historia</p>
          <h2 class="text-3xl font-black tracking-tight text-black uppercase mb-6 leading-tight" style="font-family:'Playfair Display',serif;">
            Cuidamos tu visión,<br/>cuidamos tu futuro.
          </h2>
          <p class="text-sm text-black/55 leading-relaxed mb-5">
            En Maná Óptical Betania nacimos con un propósito claro: brindar atención visual de calidad a nuestra comunidad. Ubicados en el corazón de Betania, Antioquia, somos un equipo comprometido con tu salud ocular.
          </p>
          <p class="text-sm text-black/55 leading-relaxed mb-8">
            Un examen visual a tiempo puede detectar problemas oculares antes de que afecten tu calidad de vida. Por eso recomendamos realizarse un chequeo cada 6 a 12 meses.
          </p>
          <div class="flex items-center gap-6">
            <div class="text-center">
              <div class="text-3xl font-black text-[#314037]">+500</div>
              <div class="text-[11px] tracking-widest uppercase text-black/40 mt-1">Clientes</div>
            </div>
            <div class="w-px h-12 bg-black/10" />
            <div class="text-center">
              <div class="text-3xl font-black text-[#314037]">6–12</div>
              <div class="text-[11px] tracking-widest uppercase text-black/40 mt-1">Meses entre chequeos</div>
            </div>
            <div class="w-px h-12 bg-black/10" />
            <div class="text-center">
              <div class="text-3xl font-black text-[#314037]">100%</div>
              <div class="text-[11px] tracking-widest uppercase text-black/40 mt-1">Compromiso</div>
            </div>
          </div>
        </div>

        <div v-scroll-reveal="{ direction: 'left' }" class="relative overflow-hidden h-[420px]">
          <img
            src="https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?auto=format&fit=crop&w=800&q=80"
            alt="Maná Óptical"
            class="w-full h-full object-cover"
          />
          <div class="absolute inset-0 bg-gradient-to-t from-[#314037]/40 to-transparent" />
        </div>
      </div>
    </section>

    <!-- Parallax -->
    <ParallaxDivider
      image="https://images.unsplash.com/photo-1531746020798-e6953c6e8e04?auto=format&fit=crop&w=1600&q=80"
      quote="Cuidamos tu visión, cuidamos tu futuro"
      label="Maná Óptical — Betania, Antioquia"
    />

    <!-- Valores -->
    <section class="w-full bg-[#f8f7f5] py-24 px-8 lg:px-16">
      <div class="max-w-5xl mx-auto">
        <div v-scroll-reveal class="flex flex-col items-center text-center mb-16">
          <p class="text-[11px] tracking-[0.4em] uppercase text-[#f5d984] font-medium mb-3">Lo que nos mueve</p>
          <h2 class="text-4xl font-black tracking-tight text-black uppercase" style="font-family:'Playfair Display',serif;">
            Nuestros Valores
          </h2>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8">
          <div
            v-for="(valor, i) in valores"
            :key="valor.titulo"
            v-scroll-reveal="{ delay: i * 120 }"
            class="bg-white p-8 text-center hover:shadow-lg transition-shadow duration-500"
          >
            <div class="h-14 w-14 rounded-full bg-[#314037] flex items-center justify-center mx-auto mb-5">
              <component :is="valor.icon" class="h-6 w-6 text-[#f5d984]" />
            </div>
            <h3 class="text-sm font-black tracking-widest uppercase text-black mb-3">{{ valor.titulo }}</h3>
            <p class="text-xs text-black/45 leading-relaxed">{{ valor.desc }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA -->
    <section class="bg-[#314037] py-20 px-8 text-center">
      <p class="text-[11px] tracking-[0.4em] uppercase text-[#f5d984] mb-4">¿Listo para vernos?</p>
      <h2 class="text-3xl font-black text-white uppercase mb-6" style="font-family:'Playfair Display',serif;">
        Visítanos en Betania
      </h2>
      <p class="text-white/50 text-sm mb-8">Calle 19 #19-06 · WhatsApp: 300 526 2309</p>
      <a
        href="https://wa.me/573005262309"
        target="_blank"
        class="btn-shine inline-flex items-center gap-3 bg-[#f5d984] text-[#314037] text-[11px] font-bold tracking-[0.25em] uppercase px-10 py-4 hover:opacity-90 transition-opacity duration-300"
      >
        Escribir por WhatsApp
      </a>
    </section>

  </div>
</template>
