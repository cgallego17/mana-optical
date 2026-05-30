<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'
import { useRoute, RouterLink } from 'vue-router'
import { ShoppingCart, Heart, Eye, Tag } from 'lucide-vue-next'
import { apiFetch } from '../lib/api'
import { useSeo } from '../composables/seo'

const route  = useRoute()
const { setPage, setBreadcrumb } = useSeo()

type ProdApi = {
  id: number; nombre: string; slug: string; descripcion: string
  precio: string; precio_antes: string | null; imagen_url: string
  categoria: { id: number; nombre: string; slug: string } | null
  marca: { id: number; nombre: string; slug: string } | null
}
type Prod = { id: number; slug: string; nombre: string; categoria: string; marca: string; precio: number; precioAnterior: number | null; oferta: boolean; imagen: string }

function mapProd(p: ProdApi): Prod {
  const precio = Number(p.precio)
  const pa = p.precio_antes ? Number(p.precio_antes) : null
  return {
    id: p.id, slug: p.slug, nombre: p.nombre,
    categoria: p.categoria?.nombre ?? '—', marca: p.marca?.nombre ?? '—',
    precio, precioAnterior: pa, oferta: Boolean(pa && pa > precio),
    imagen: p.imagen_url || 'https://images.unsplash.com/photo-1574258495973-f010dfbb5371?auto=format&fit=crop&w=600&q=80',
  }
}

function formatPrecio(n: number) { return `$${n.toLocaleString('es-CO')}` }

const cargando   = ref(false)
const errorMsg   = ref('')
const productos  = ref<Prod[]>([])
const catNombre  = ref('')
const wishlist   = ref<Set<number>>(new Set())
const ordenar    = ref<'relevancia' | 'precio-asc' | 'precio-desc' | 'nombre'>('relevancia')

const prodsFiltrados = computed(() => {
  const lista = [...productos.value]
  if (ordenar.value === 'precio-asc')  lista.sort((a, b) => a.precio - b.precio)
  if (ordenar.value === 'precio-desc') lista.sort((a, b) => b.precio - a.precio)
  if (ordenar.value === 'nombre')      lista.sort((a, b) => a.nombre.localeCompare(b.nombre))
  return lista
})

async function cargar(slug: string) {
  cargando.value = true; errorMsg.value = ''
  try {
    const data = await apiFetch<ProdApi[] | { results: ProdApi[] }>(
      `/catalogo/productos/?categoria=${encodeURIComponent(slug)}`
    )
    const lista = Array.isArray(data) ? data : data.results
    productos.value = lista.map(mapProd)
    catNombre.value = lista[0]?.categoria?.nombre ?? slug
    setPage({
      title: `${catNombre.value} | Tienda Maná Óptical`,
      description: `Explora nuestra colección de ${catNombre.value.toLowerCase()} en Maná Óptical.`,
    })
    setBreadcrumb([
      { name: 'Inicio', url: `${window.location.origin}/` },
      { name: 'Tienda', url: `${window.location.origin}/tienda` },
      { name: catNombre.value, url: window.location.href },
    ])
  } catch (e) { errorMsg.value = e instanceof Error ? e.message : 'Error'
  } finally { cargando.value = false }
}

watch(() => route.params.slug, (slug) => { if (typeof slug === 'string') cargar(slug) })
onMounted(() => { const slug = route.params.slug; if (typeof slug === 'string') cargar(slug) })

function toggleWishlist(id: number) {
  const s = new Set(wishlist.value); s.has(id) ? s.delete(id) : s.add(id); wishlist.value = s
}
</script>

<template>
  <div style="padding-top: var(--header-h, 4rem)">

    <!-- Hero -->
    <div class="bg-[#314037] py-12 px-6 text-center">
      <p class="text-[11px] tracking-[0.4em] uppercase text-[#f5d984] mb-2">Tienda</p>
      <h1 class="text-3xl sm:text-4xl lg:text-5xl font-black text-white uppercase tracking-tight"
          style="font-family:'Playfair Display',serif;">
        {{ catNombre || route.params.slug }}
      </h1>
    </div>

    <!-- Breadcrumb -->
    <div class="border-b border-black/[0.06] bg-[#f8f7f5]">
      <div class="max-w-screen-xl mx-auto px-4 sm:px-6 lg:px-8 py-3 flex items-center gap-2 text-[11px] text-black/40">
        <RouterLink to="/" class="hover:text-black transition">Inicio</RouterLink>
        <span>/</span>
        <RouterLink to="/tienda" class="hover:text-black transition">Tienda</RouterLink>
        <span>/</span>
        <span class="text-black/70 font-semibold">{{ catNombre || route.params.slug }}</span>
      </div>
    </div>

    <div class="max-w-screen-xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
      <div v-if="errorMsg" class="mb-6 border border-red-200 bg-red-50 px-4 py-3 text-[11px] text-red-700">{{ errorMsg }}</div>

      <!-- Top bar -->
      <div class="flex items-center justify-between mb-8 flex-wrap gap-3">
        <p class="text-[11px] text-black/40">
          <template v-if="!cargando">{{ prodsFiltrados.length }} {{ prodsFiltrados.length === 1 ? 'producto' : 'productos' }}</template>
          <template v-else>Cargando…</template>
        </p>
        <select v-model="ordenar"
          class="appearance-none pl-3 pr-8 py-2 text-[11px] font-semibold border border-black/15 outline-none focus:border-[#314037] bg-white cursor-pointer">
          <option value="relevancia">Relevancia</option>
          <option value="precio-asc">Menor precio</option>
          <option value="precio-desc">Mayor precio</option>
          <option value="nombre">Nombre A–Z</option>
        </select>
      </div>

      <!-- Grid -->
      <div class="grid grid-cols-2 md:grid-cols-3 xl:grid-cols-4 gap-x-4 gap-y-8 sm:gap-x-6 sm:gap-y-10">
        <div v-for="p in prodsFiltrados" :key="p.id" class="group">
          <div class="relative bg-[#f8f7f5] overflow-hidden mb-3">
            <RouterLink :to="`/producto/${p.slug}`" class="block">
              <div class="h-44 sm:h-52 flex items-center justify-center p-4 sm:p-6">
                <img :src="p.imagen" :alt="p.nombre" loading="lazy"
                  class="h-full w-full object-contain transition-transform duration-700 group-hover:scale-105" />
              </div>
            </RouterLink>
            <span v-if="p.oferta"
              class="absolute top-2.5 left-2.5 bg-[#314037] text-[#f5d984] text-[9px] font-bold tracking-widest uppercase px-2.5 py-1">
              Oferta
            </span>
            <button @click="toggleWishlist(p.id)"
              class="absolute top-2.5 right-2.5 h-7 w-7 flex items-center justify-center bg-white/90 backdrop-blur-sm shadow-sm transition hover:bg-white"
              :aria-label="wishlist.has(p.id) ? 'Quitar de favoritos' : 'Agregar a favoritos'">
              <Heart class="h-3.5 w-3.5 transition-colors"
                :class="wishlist.has(p.id) ? 'fill-[#314037] text-[#314037]' : 'text-black/40'" />
            </button>
            <div class="absolute inset-x-0 bottom-0 flex translate-y-full group-hover:translate-y-0 transition-transform duration-300">
              <RouterLink :to="`/producto/${p.slug}`"
                class="flex-1 bg-white/95 text-black text-[10px] font-bold tracking-widest uppercase py-2.5 hover:bg-[#f5d984] transition-colors flex items-center justify-center gap-1.5 border-r border-black/8">
                <Eye class="h-3.5 w-3.5" /> Ver
              </RouterLink>
              <button class="flex-1 bg-[#314037] text-white text-[10px] font-bold tracking-widest uppercase py-2.5 hover:bg-[#f5d984] hover:text-[#314037] transition-colors flex items-center justify-center gap-1.5">
                <ShoppingCart class="h-3.5 w-3.5" /> Carrito
              </button>
            </div>
          </div>
          <div class="text-center px-1">
            <p class="text-[9px] tracking-widest uppercase text-black/30 mb-1">{{ p.categoria }}</p>
            <RouterLink :to="`/producto/${p.slug}`" class="block">
              <h3 class="text-[12px] sm:text-sm font-bold tracking-wide uppercase text-black hover:text-[#314037] transition-colors mb-2 leading-tight">{{ p.nombre }}</h3>
            </RouterLink>
            <div class="flex items-center justify-center gap-2">
              <span v-if="p.precioAnterior" class="text-xs line-through text-black/25">{{ formatPrecio(p.precioAnterior) }}</span>
              <span class="text-sm font-black text-[#314037]">{{ formatPrecio(p.precio) }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Vacío -->
      <div v-if="!cargando && prodsFiltrados.length === 0" class="text-center py-24 text-black/30">
        <Tag class="h-10 w-10 mx-auto mb-4 opacity-25" />
        <p class="text-sm font-semibold">No hay productos en esta categoría.</p>
        <RouterLink to="/tienda" class="mt-4 inline-block text-[11px] font-bold tracking-widest uppercase underline underline-offset-4 hover:text-black transition">
          Ver toda la tienda
        </RouterLink>
      </div>
    </div>

  </div>
</template>
