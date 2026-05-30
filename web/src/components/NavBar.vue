<script setup lang="ts">
import { ref, nextTick, onMounted, onUnmounted, watch } from 'vue'
import { Menu, X, Heart, User, ShoppingCart, Search, Facebook, Instagram, Mail, MapPin, Phone, Clock } from 'lucide-vue-next'
import { useSearchOverlay } from '../composables/searchOverlay'

const menuOpen = ref(false)
const scrolled = ref(false)
const scrollProgress = ref(0)
const headerEl = ref<HTMLElement | null>(null)
const headerH = ref(64)  // fallback razonable en px
let ro: ResizeObserver | null = null

const measure = () => {
  const h = headerEl.value?.getBoundingClientRect().height ?? 0
  if (h > 0) {
    headerH.value = h
    document.documentElement.style.setProperty('--header-h', `${h}px`)
  }
}

const onScroll = () => {
  scrolled.value = window.scrollY > 60
  const total = document.documentElement.scrollHeight - window.innerHeight
  scrollProgress.value = total > 0 ? (window.scrollY / total) * 100 : 0
}

const onKeydown = (e: KeyboardEvent) => {
  if (e.key === 'Escape') menuOpen.value = false
}

onMounted(async () => {
  await nextTick()
  measure()
  // Reintentar luego del primer paint por si getBoundingClientRect devuelve 0
  requestAnimationFrame(measure)
  setTimeout(measure, 100)

  window.addEventListener('scroll', onScroll, { passive: true })
  window.addEventListener('resize', measure)
  window.addEventListener('keydown', onKeydown)

  if ('ResizeObserver' in window) {
    ro = new ResizeObserver(measure)
    if (headerEl.value) ro.observe(headerEl.value)
  }
})
onUnmounted(() => {
  window.removeEventListener('scroll', onScroll)
  window.removeEventListener('resize', measure)
  window.removeEventListener('keydown', onKeydown)
  if (ro) { ro.disconnect(); ro = null }
})

const nav = [
  { to: '/',          label: 'INICIO' },
  { to: '/servicios', label: 'SERVICIOS' },
  { to: '/tienda',    label: 'TIENDA' },
  { to: '/galeria',   label: 'GALERÍA' },
  { to: '/blog',      label: 'BLOG' },
  { to: '/nosotros',  label: 'NOSOTROS' },
  { to: '/contacto',  label: 'CONTACTO' },
  { to: '/agenda',    label: 'AGENDA' },
]

const { open: openSearch, isOpen: searchOpen } = useSearchOverlay()

// Bloquear scroll del body (sin tocar html para evitar pantalla en blanco)
watch(menuOpen, (val) => {
  document.body.style.overflow = val ? 'hidden' : ''
})
watch(searchOpen, (val) => { if (val) menuOpen.value = false })
// Actualizar altura cuando cambia el menú (barra superior puede colapsar)
watch(menuOpen, () => setTimeout(measure, 50))
</script>

<template>
  <!-- Barra de progreso de scroll -->
  <div
    class="fixed top-0 left-0 z-[40] h-[3px] bg-[#f5d984] transition-all duration-150 ease-out pointer-events-none"
    :style="{ width: scrollProgress + '%' }"
  />

  <!-- Header: z-[90] para quedar ENCIMA del drawer (z-[85]) -->
  <header
    ref="headerEl"
    class="fixed inset-x-0 top-0 z-[90] transition-all duration-500"
    :class="scrolled ? 'bg-white/95 backdrop-blur-md shadow-sm' : 'bg-white'"
  >
    <!-- Barra superior de información (sm+, colapsa al hacer scroll) -->
    <div
      class="hidden sm:block bg-[#314037] overflow-hidden transition-[max-height,opacity] duration-500"
      :class="scrolled ? 'max-h-0 opacity-0 pointer-events-none' : 'max-h-16 opacity-100'"
    >
      <div class="flex items-center justify-between px-4 sm:px-6 lg:px-8 py-2">
        <div class="flex items-center gap-3 text-[11px]">
          <a href="#" aria-label="Facebook" class="text-[#f5d984] hover:opacity-70 transition"><Facebook class="h-3.5 w-3.5" /></a>
          <a href="#" aria-label="Instagram" class="text-[#f5d984] hover:opacity-70 transition"><Instagram class="h-3.5 w-3.5" /></a>
          <a href="mailto:manaoptical2@gmail.com" class="hidden md:inline-flex items-center gap-1.5 text-white/60 hover:text-white transition">
            <Mail class="h-3.5 w-3.5 text-[#f5d984]" /><span>manaoptical2@gmail.com</span>
          </a>
        </div>
        <div class="flex items-center gap-4 text-[11px] text-white/60">
          <span class="hidden lg:inline-flex items-center gap-1.5">
            <MapPin class="h-3.5 w-3.5 text-[#f5d984] shrink-0" />Calle 19 #19-06, Betania
          </span>
          <span class="inline-flex items-center gap-1.5">
            <Phone class="h-3.5 w-3.5 text-[#f5d984] shrink-0" />300 526 2309
          </span>
          <span class="hidden sm:inline-flex items-center gap-1.5">
            <Clock class="h-3.5 w-3.5 text-[#f5d984] shrink-0" />Lun–Sáb: 9AM–9PM
          </span>
        </div>
      </div>
    </div>

    <!-- Barra principal -->
    <nav class="border-b border-black/[0.08]">
      <div
        class="flex items-center justify-between px-4 sm:px-6 lg:px-8 transition-all duration-500"
        :class="scrolled ? 'py-2' : 'py-3'"
      >
        <!-- Logo -->
        <RouterLink to="/" class="flex items-center gap-2.5 shrink-0 transition hover:opacity-80">
          <img src="/logo.png" alt="Optica Mana" class="h-9 sm:h-10 w-auto object-contain" />
          <span class="hidden xl:block text-[9px] leading-tight tracking-[0.28em] text-black/60 font-semibold uppercase">
            Visión con<br>Propósito
          </span>
        </RouterLink>

        <!-- Links (solo lg+) -->
        <div class="hidden lg:flex items-center gap-5 xl:gap-7">
          <RouterLink
            v-for="item in nav"
            :key="item.to"
            :to="item.to"
            class="relative pb-0.5 text-[10.5px] xl:text-[11px] font-semibold tracking-[0.18em] whitespace-nowrap text-black/65 hover:text-black transition"
            active-class="!text-black after:absolute after:bottom-0 after:left-0 after:right-0 after:h-0.5 after:bg-[#f5d984]"
            exact-active-class="!text-black after:absolute after:bottom-0 after:left-0 after:right-0 after:h-0.5 after:bg-[#f5d984]"
          >
            {{ item.label }}
          </RouterLink>
        </div>

        <!-- Iconos derecha -->
        <div class="flex items-center shrink-0">
          <button
            aria-label="Buscar"
            class="p-2 rounded-md text-black/50 hover:text-black hover:bg-black/5 transition"
            @click="openSearch()"
          >
            <Search class="h-4 w-4 sm:h-5 sm:w-5" />
          </button>
          <button
            aria-label="Favoritos"
            class="relative hidden sm:flex p-2 rounded-md text-black/50 hover:text-black hover:bg-black/5 transition"
          >
            <Heart class="h-4 w-4 sm:h-5 sm:w-5" />
            <span class="absolute top-1 right-1 h-3.5 w-3.5 rounded-full bg-[#314037] text-[8px] text-white flex items-center justify-center font-bold leading-none">0</span>
          </button>
          <RouterLink
            to="/cuenta"
            aria-label="Mi cuenta"
            class="hidden sm:flex p-2 rounded-md text-black/50 hover:text-black hover:bg-black/5 transition"
          >
            <User class="h-4 w-4 sm:h-5 sm:w-5" />
          </RouterLink>
          <RouterLink
            to="/carrito"
            aria-label="Carrito"
            class="relative flex p-2 rounded-md text-black/50 hover:text-black hover:bg-black/5 transition"
          >
            <ShoppingCart class="h-4 w-4 sm:h-5 sm:w-5" />
            <span class="absolute top-1 right-1 h-3.5 w-3.5 rounded-full bg-[#314037] text-[8px] text-white flex items-center justify-center font-bold leading-none">0</span>
          </RouterLink>
          <button
            class="lg:hidden ml-0.5 p-2 rounded-md text-black/50 hover:text-black hover:bg-black/5 transition"
            :aria-label="menuOpen ? 'Cerrar menú' : 'Abrir menú'"
            @click="menuOpen = !menuOpen"
          >
            <component :is="menuOpen ? X : Menu" class="h-5 w-5" />
          </button>
        </div>
      </div>
    </nav>
  </header>

  <!-- Drawer móvil: cubre pantalla completa (z-85, DEBAJO del header z-90) -->
  <transition name="fade">
    <div
      v-if="menuOpen"
      class="fixed inset-0 z-[85] lg:hidden"
    >
      <!-- Backdrop oscuro -->
      <div class="absolute inset-0 bg-black/50" @click="menuOpen = false" />

      <!-- Panel lateral -->
      <transition name="slide">
        <div
          class="absolute right-0 top-0 h-full w-4/5 max-w-xs bg-white shadow-2xl flex flex-col"
          :style="{ paddingTop: headerH + 'px' }"
        >
          <!-- Nav links -->
          <div class="flex-1 overflow-y-auto">
            <nav class="flex flex-col gap-0.5 px-3 py-3">
              <RouterLink
                v-for="item in nav"
                :key="item.to"
                :to="item.to"
                class="flex items-center rounded-lg px-4 py-3.5 text-[11.5px] font-bold tracking-[0.2em] text-black/70 hover:text-[#314037] hover:bg-[#f8f7f4] transition-colors"
                active-class="!text-[#314037] bg-[#f8f7f4]"
                @click="menuOpen = false"
              >
                {{ item.label }}
              </RouterLink>
            </nav>

            <!-- Accesos rápidos (Favoritos + Cuenta, ocultos en header móvil) -->
            <div class="border-t border-black/[0.08] flex gap-1 px-3 py-3">
              <button
                class="flex-1 flex items-center justify-center gap-2 rounded-lg py-2.5 text-[11px] font-semibold text-black/55 hover:text-black hover:bg-black/5 transition-colors"
                aria-label="Favoritos"
              >
                <Heart class="h-4 w-4" /> Favoritos
              </button>
              <RouterLink
                to="/cuenta"
                class="flex-1 flex items-center justify-center gap-2 rounded-lg py-2.5 text-[11px] font-semibold text-black/55 hover:text-black hover:bg-black/5 transition-colors"
                @click="menuOpen = false"
              >
                <User class="h-4 w-4" /> Mi cuenta
              </RouterLink>
            </div>
          </div>

          <!-- Información de contacto -->
          <div class="border-t border-black/[0.08] bg-[#f8f7f4] px-5 py-4 space-y-2.5 shrink-0">
            <p class="text-[9px] font-black tracking-[0.28em] uppercase text-[#314037]/60 mb-3">Contáctanos</p>
            <div class="flex items-center gap-2.5 text-[11.5px] text-black/60">
              <Phone class="h-3.5 w-3.5 text-[#314037] shrink-0" /><span>300 526 2309</span>
            </div>
            <div class="flex items-start gap-2.5 text-[11.5px] text-black/60">
              <MapPin class="h-3.5 w-3.5 text-[#314037] shrink-0 mt-0.5" /><span>Calle 19 #19-06, Betania, Antioquia</span>
            </div>
            <div class="flex items-center gap-2.5 text-[11.5px] text-black/60">
              <Clock class="h-3.5 w-3.5 text-[#314037] shrink-0" /><span>Lun–Sáb: 9AM–9PM</span>
            </div>
          </div>

          <!-- Redes sociales -->
          <div
            class="border-t border-black/[0.08] flex items-center gap-4 px-5 py-4 shrink-0"
            style="padding-bottom: calc(1rem + env(safe-area-inset-bottom))"
          >
            <a href="#" aria-label="Facebook" class="text-[#314037] hover:opacity-60 transition"><Facebook class="h-4 w-4" /></a>
            <a href="#" aria-label="Instagram" class="text-[#314037] hover:opacity-60 transition"><Instagram class="h-4 w-4" /></a>
            <a
              href="mailto:manaoptical2@gmail.com"
              class="ml-auto flex items-center gap-1.5 text-[10.5px] text-black/45 hover:text-black transition"
            >
              <Mail class="h-3.5 w-3.5" />manaoptical2@gmail.com
            </a>
          </div>
        </div>
      </transition>
    </div>
  </transition>
</template>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity .2s ease }
.fade-enter-from, .fade-leave-to { opacity: 0 }

.slide-enter-active, .slide-leave-active { transition: transform .25s cubic-bezier(0.4, 0, 0.2, 1) }
.slide-enter-from, .slide-leave-to { transform: translateX(100%) }
</style>
