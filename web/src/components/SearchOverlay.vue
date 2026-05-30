<script setup lang="ts">
import { ref, watch, onMounted, onUnmounted } from 'vue'
import { X, Search } from 'lucide-vue-next'
import { useSearchOverlay } from '../composables/searchOverlay'
import { apiFetch } from '../lib/api'

const { isOpen, query, close } = useSearchOverlay()

const results = ref<Array<{ title: string; subtitle: string; href: string }>>([])
const isLoading = ref(false)
const error = ref<string | null>(null)
let debounceId: number | undefined

async function runSearch(q: string) {
  const t = q.trim()
  if (!t) {
    results.value = []
    error.value = null
    isLoading.value = false
    return
  }

  isLoading.value = true
  error.value = null

  try {
    const data = await apiFetch<{ q: string; results: Array<{ title: string; subtitle: string; href: string }> }>(
      `/busqueda/?q=${encodeURIComponent(t)}`,
    )
    results.value = data.results
  } catch (e) {
    results.value = []
    error.value = e instanceof Error ? e.message : String(e)
  } finally {
    isLoading.value = false
  }
}

watch(query, (q) => {
  if (debounceId) window.clearTimeout(debounceId)
  debounceId = window.setTimeout(() => runSearch(q), 180)
})

function onKey(e: KeyboardEvent) {
  if (e.key === 'Escape' && isOpen.value) {
    e.preventDefault(); close()
  }
}

onMounted(() => window.addEventListener('keydown', onKey))
onUnmounted(() => window.removeEventListener('keydown', onKey))
</script>

<template>
  <transition name="fade">
    <div
      v-if="isOpen"
      class="fixed inset-0 z-[90]"
      aria-modal="true"
      role="dialog"
    >
      <!-- Backdrop -->
      <div class="absolute inset-0 bg-black/50 backdrop-blur-[2px]" @click="close" />

      <!-- Panel -->
      <div class="relative mx-auto mt-24 w-full max-w-2xl px-4">
        <div class="overflow-hidden rounded-sm border border-black/10 bg-white shadow-2xl">
          <div class="flex items-center gap-3 border-b border-black/10 px-4 py-3">
            <Search class="h-4 w-4 text-black/40" />
            <input
              autofocus
              v-model="query"
              type="search"
              placeholder="Busca productos, servicios o artículos (Ctrl/⌘+K)"
              class="w-full bg-transparent text-sm outline-none placeholder:text-black/40"
            />
            <button class="text-black/50 hover:text-black" aria-label="Cerrar" @click="close">
              <X class="h-5 w-5" />
            </button>
          </div>

          <div class="max-h-80 overflow-auto">
            <div v-if="!query" class="px-5 py-6 text-sm text-black/50">
              Empieza a escribir para buscar. Sugerencias: examen, monturas, agenda, contacto.
            </div>
            <ul v-else>
              <li v-if="isLoading" class="px-5 py-6 text-sm text-black/50">
                Buscando...
              </li>
              <li v-else-if="error" class="px-5 py-6 text-sm text-black/50">
                {{ error }}
              </li>
              <li v-for="item in results" :key="item.href">
                <RouterLink
                  :to="item.href"
                  class="flex items-start justify-between gap-4 px-5 py-3 hover:bg-[#f8f7f5] transition-colors"
                  @click="close()"
                >
                  <div>
                    <div class="text-sm font-semibold text-black">{{ item.title }}</div>
                    <div class="text-xs text-black/50">{{ item.subtitle }}</div>
                  </div>
                  <span class="text-[10px] tracking-widest uppercase text-black/30">Abrir</span>
                </RouterLink>
              </li>
              <li v-if="!isLoading && !error && results.length === 0" class="px-5 py-6 text-sm text-black/50">
                No encontramos resultados para "{{ query }}".
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </transition>
</template>

<style scoped>
.fade-enter-active,.fade-leave-active{ transition: opacity .2s ease }
.fade-enter-from,.fade-leave-to{ opacity: 0 }
</style>
