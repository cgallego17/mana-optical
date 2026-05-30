<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { useSearchOverlay } from '../composables/searchOverlay'

const visible = ref(false)
const { isOpen } = useSearchOverlay()

const stylePos = computed(() => ({
  bottom: `clamp(56px, calc(5rem + env(safe-area-inset-bottom)), 96px)`,
  right: `clamp(8px, calc(1rem + env(safe-area-inset-right)), 24px)`,
}))

function onScroll() {
  visible.value = window.scrollY > 240
}

function scrollTop() {
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

onMounted(() => window.addEventListener('scroll', onScroll, { passive: true }))
onUnmounted(() => window.removeEventListener('scroll', onScroll))
</script>

<template>
  <button
    v-show="visible && !isOpen"
    class="fab fixed z-[49] inline-flex items-center justify-center h-12 w-12 rounded-full border border-[#D4AF37]/30 bg-white text-[#314037] shadow-[0_12px_30px_rgba(0,0,0,0.2)] hover:translate-y-[-2px] transition-all overflow-hidden"
    :style="stylePos"
    aria-label="Volver arriba"
    @click="scrollTop"
  >
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" class="h-5 w-5">
      <path d="M12 19V5" />
      <path d="m5 12 7-7 7 7" />
    </svg>
  </button>
</template>

<style scoped>
@media (max-width: 380px) {
  button.fab { width: 2.5rem; height: 2.5rem; }
}

/* Ocultar FAB cuando el body/html tienen overflow-hidden (menú móvil u overlay bloqueando scroll) */
:global(html.overflow-hidden) button.fab,
:global(body.overflow-hidden) button.fab { display: none !important; }
</style>
