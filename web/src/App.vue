<script setup lang="ts">
import { onMounted, onUnmounted } from 'vue'
import NavBar from './components/NavBar.vue'
import Footer from './components/Footer.vue'
import WhatsAppFab from './components/WhatsAppFab.vue'
import SearchOverlay from './components/SearchOverlay.vue'
import BackToTop from './components/BackToTop.vue'
import AgendaModal from './components/AgendaModal.vue'
import { useSearchOverlay } from './composables/searchOverlay'
import { useAgendaModal } from './composables/agendaModal'

const { open } = useSearchOverlay()
const { open: openAgenda } = useAgendaModal()

// Escuchar evento global para abrir agenda desde cualquier componente
if (typeof window !== 'undefined') {
  window.addEventListener('open-agenda', () => openAgenda())
}

function onKeydown(e: KeyboardEvent) {
  const isCmdK = (e.ctrlKey || e.metaKey) && (e.key.toLowerCase() === 'k')
  if (isCmdK) {
    e.preventDefault()
    open()
  }
}

onMounted(() => window.addEventListener('keydown', onKeydown))
onUnmounted(() => window.removeEventListener('keydown', onKeydown))
</script>

<template>
  <div class="min-h-screen bg-white">
    <NavBar />
    <RouterView />
    <SearchOverlay />
    <AgendaModal />
    <BackToTop />
    <WhatsAppFab />
    <Footer />
  </div>
</template>
