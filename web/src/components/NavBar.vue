<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { Menu, X, Heart, User, ShoppingCart, Search, Facebook, Twitter, Instagram, Mail, MapPin, Phone, Clock } from 'lucide-vue-next'

const open = ref(false)
const scrolled = ref(false)
const scrollProgress = ref(0)

const onScroll = () => {
  scrolled.value = window.scrollY > 60
  const total = document.documentElement.scrollHeight - window.innerHeight
  scrollProgress.value = total > 0 ? (window.scrollY / total) * 100 : 0
}

onMounted(() => window.addEventListener('scroll', onScroll, { passive: true }))
onUnmounted(() => window.removeEventListener('scroll', onScroll))

const nav = [
  { to: '/',         label: 'INICIO' },
  { to: '/paginas',  label: 'PÁGINAS' },
  { to: '/tienda',   label: 'TIENDA' },
  { to: '/blog',     label: 'BLOG' },
  { to: '/nosotros', label: 'NOSOTROS' },
]
</script>

<template>
  <!-- Scroll progress bar -->
  <div
    class="fixed top-0 left-0 z-[60] h-[3px] bg-[#f5d984] transition-all duration-150 ease-out"
    :style="{ width: scrollProgress + '%' }"
  />

  <header
    class="fixed inset-x-0 top-0 z-50 transition-all duration-500"
    :class="scrolled
      ? 'bg-white/95 backdrop-blur-md shadow-sm pt-0'
      : 'bg-white pt-10'"
  >
    <!-- Top Info Bar — hidden when scrolled -->
    <div
      class="absolute inset-x-0 top-0 bg-[#314037] py-2 transition-all duration-500"
      :class="scrolled ? 'opacity-0 -translate-y-full pointer-events-none' : 'opacity-100 translate-y-0'"
    >
      <div class="flex w-full flex-col gap-3 px-4 text-[11px] text-white/50 sm:flex-row sm:items-center sm:justify-between sm:px-6 lg:px-8">
        <div class="flex items-center gap-4">
          <a href="#" class="inline-flex items-center gap-1.5 text-[#f5d984] hover:opacity-70 transition"><Facebook class="h-3.5 w-3.5" /></a>
          <a href="#" class="inline-flex items-center gap-1.5 text-[#f5d984] hover:opacity-70 transition"><Twitter class="h-3.5 w-3.5" /></a>
          <a href="#" class="inline-flex items-center gap-1.5 text-[#f5d984] hover:opacity-70 transition"><Instagram class="h-3.5 w-3.5" /></a>
          <a href="mailto:manaoptical2@gmail.com" class="inline-flex items-center gap-1.5 text-white/50 hover:text-white transition">
            <Mail class="h-3.5 w-3.5 text-[#f5d984]" /> manaoptical2@gmail.com
          </a>
        </div>
        <div class="flex flex-col gap-2 sm:flex-row sm:items-center sm:gap-6">
          <span class="inline-flex items-center gap-1.5"><MapPin class="h-3.5 w-3.5 text-[#f5d984]" />Calle 19 #19-06, Betania, Antioquia</span>
          <span class="inline-flex items-center gap-1.5"><Phone class="h-3.5 w-3.5 text-[#f5d984]" />WhatsApp: 300 526 2309</span>
          <span class="inline-flex items-center gap-1.5"><Clock class="h-3.5 w-3.5 text-[#f5d984]" />Lun–Sáb: 9AM–9PM</span>
        </div>
      </div>
    </div>

    <!-- Main Nav -->
    <nav class="border-b border-black/8 bg-transparent">
      <div class="w-full px-6 lg:px-8 transition-all duration-500" :class="scrolled ? 'py-3' : 'py-4'">
        <div class="flex items-center justify-between">

          <!-- Logo -->
          <a href="#" class="flex flex-col items-start transition hover:opacity-80">
            <img src="/logo.png" alt="Optica Mana" class="h-10 w-auto object-contain" />
            <span class="text-[9px] tracking-[0.3em] text-black/70 font-semibold uppercase mt-0.5">Visión con Propósito</span>
          </a>

          <!-- Desktop Nav -->
          <div class="hidden items-center gap-10 md:flex">
            <RouterLink
              v-for="item in nav"
              :key="item.to"
              :to="item.to"
              class="text-[11px] font-semibold tracking-[0.2em] transition pb-0.5 relative text-black/70 hover:text-black"
              active-class="!text-black font-bold after:absolute after:bottom-0 after:left-0 after:right-0 after:h-0.5 after:bg-[#f5d984]"
              exact-active-class="!text-black font-bold after:absolute after:bottom-0 after:left-0 after:right-0 after:h-0.5 after:bg-[#f5d984]"
            >
              {{ item.label }}
            </RouterLink>
          </div>

          <!-- Right Icons -->
          <div class="flex items-center gap-5">
            <button class="text-black/50 transition hover:text-black"><Search class="h-4 w-4" /></button>
            <button class="relative text-black/50 transition hover:text-black">
              <Heart class="h-4 w-4" />
              <span class="absolute -top-2 -right-2 h-4 w-4 rounded-full bg-[#314037] text-[9px] text-white flex items-center justify-center font-bold">0</span>
            </button>
            <button class="text-black/50 transition hover:text-black"><User class="h-4 w-4" /></button>
            <button class="relative text-black/50 transition hover:text-black">
              <ShoppingCart class="h-4 w-4" />
              <span class="absolute -top-2 -right-2 h-4 w-4 rounded-full bg-[#314037] text-[9px] text-white flex items-center justify-center font-bold">0</span>
            </button>
            <button class="md:hidden text-black/50 transition hover:text-black" @click="open = !open">
              <component :is="open ? X : Menu" class="h-5 w-5" />
            </button>
          </div>
        </div>
      </div>
    </nav>
  </header>
</template>
