<script setup lang="ts">
import { Instagram, Facebook, Twitter, Mail, Phone, MapPin } from 'lucide-vue-next'

const brands = ['Bionic', 'Vision', 'Eye–Blue', 'Optical', 'Wear']

const links = [
  {
    heading: 'Servicios',
    items: ['Reservar examen visual', 'Terapia visual', 'Vouchers', 'Lentes y precios', 'Salud ocular'],
  },
  {
    heading: 'La Empresa',
    items: ['Contacto', 'Preguntas frecuentes', 'Envíos', 'Tiendas', 'Colección', 'Trabaja con nosotros'],
  },
  {
    heading: 'General',
    items: ['Nuestros doctores', 'Sobre nosotros', 'Productos', 'Productos en oferta', 'Noticias'],
  },
]
</script>

<template>
  <footer class="w-full">

    <!-- Brands bar -->
    <div class="bg-[#f8f7f5] border-y border-black/6 py-8 px-6 lg:px-16 overflow-hidden">
      <div class="flex flex-wrap items-center justify-center gap-x-8 gap-y-3 max-w-6xl mx-auto">
        <span
          v-for="brand in brands"
          :key="brand"
          class="text-sm lg:text-lg font-bold tracking-[0.25em] lg:tracking-[0.3em] text-black/20 uppercase select-none hover:text-black/40 transition-colors duration-300 cursor-default whitespace-nowrap"
          style="font-family: 'Playfair Display', serif;"
        >
          {{ brand }}
        </span>
      </div>
    </div>

    <!-- Main footer -->
    <div class="bg-[#314037] px-8 lg:px-16 py-20">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-14 max-w-6xl mx-auto">

        <!-- Brand col -->
        <div class="space-y-6">
          <!-- Logo + slogan -->
          <div>
            <img src="/logo-amarillo.png" alt="Optica Mana" class="h-12 w-auto object-contain mb-2" />
            <p class="text-[10px] tracking-[0.35em] uppercase text-[#f5d984] font-semibold">Visión con Propósito</p>
          </div>

          <!-- Divider -->
          <div class="w-10 h-0.5 bg-[#f5d984]/40" />

          <!-- Descripción -->
          <p class="text-xs text-white/50 leading-loose">
            En Maná Optical Betania estamos comprometidos con tu salud visual y el bienestar de nuestra gente.
          </p>

          <!-- Contacto -->
          <div class="space-y-3 pt-1">
            <a href="mailto:manaoptical2@gmail.com"
               class="flex items-center gap-3 text-xs text-white/60 hover:text-[#f5d984] transition-colors duration-300 group">
              <Mail class="h-3.5 w-3.5 text-[#f5d984] flex-shrink-0" />
              manaoptical2@gmail.com
            </a>
            <a href="https://wa.me/573005262309" target="_blank"
               class="flex items-center gap-3 text-xs text-white/60 hover:text-[#f5d984] transition-colors duration-300">
              <Phone class="h-3.5 w-3.5 text-[#f5d984] flex-shrink-0" />
              300 526 2309
            </a>
            <div class="flex items-start gap-3 text-xs text-white/60">
              <MapPin class="h-3.5 w-3.5 text-[#f5d984] flex-shrink-0 mt-0.5" />
              Calle 19 #19-06<br/>Betania, Antioquia
            </div>
          </div>
        </div>

        <!-- Link columns -->
        <div v-for="col in links" :key="col.heading">
          <h4 class="text-[11px] font-black tracking-[0.3em] uppercase text-[#f5d984] mb-6 pb-3 border-b border-[#f5d984]/20">
            {{ col.heading }}
          </h4>
          <ul class="space-y-3">
            <li v-for="item in col.items" :key="item">
              <a href="#" class="text-sm text-white/45 hover:text-white hover:pl-1 transition-all duration-200">
                {{ item }}
              </a>
            </li>
          </ul>
        </div>

      </div>
    </div>

    <!-- Bottom bar -->
    <div class="bg-[#f5d984] px-8 lg:px-16 py-5">
      <div class="flex items-center justify-between max-w-6xl mx-auto">
        <div class="flex items-center gap-5">
          <a href="#" class="text-[#314037] hover:opacity-70 transition"><Instagram class="h-4 w-4" /></a>
          <a href="#" class="text-[#314037] hover:opacity-70 transition"><Facebook class="h-4 w-4" /></a>
          <a href="#" class="text-[#314037] hover:opacity-70 transition">
            <svg class="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22" />
            </svg>
          </a>
          <a href="#" class="text-[#314037] hover:opacity-70 transition"><Twitter class="h-4 w-4" /></a>
        </div>
        <p class="text-[11px] text-[#314037] tracking-widest uppercase font-semibold">
          © 2026 Maná Óptical — Realizado por <a href="https://megadominio.co" target="_blank" class="underline hover:opacity-70 transition">Megadominio.co</a> — Todos los derechos reservados
        </p>
      </div>
    </div>

  </footer>
</template>
