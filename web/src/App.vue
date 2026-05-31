<script setup lang="ts">
import { onMounted, onUnmounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import NavBar from './components/NavBar.vue'
import Footer from './components/Footer.vue'
import WhatsAppFab from './components/WhatsAppFab.vue'
import SearchOverlay from './components/SearchOverlay.vue'
import BackToTop from './components/BackToTop.vue'
import AgendaModal from './components/AgendaModal.vue'
import { useSearchOverlay } from './composables/searchOverlay'
import { useAgendaModal } from './composables/agendaModal'
import { useSeo } from './composables/seo'

const { open } = useSearchOverlay()
const { open: openAgenda } = useAgendaModal()
const { setOrganization } = useSeo()

setOrganization()

const route = useRoute()
const isAdminRoute = computed(() => String(route.path || '').startsWith('/panel'))

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
    <NavBar v-if="!isAdminRoute" />
    <RouterView />
    <SearchOverlay v-if="!isAdminRoute" />
    <AgendaModal v-if="!isAdminRoute" />
    <BackToTop v-if="!isAdminRoute" />
    <WhatsAppFab v-if="!isAdminRoute" />
    <Footer v-if="!isAdminRoute" />
  </div>
</template>
