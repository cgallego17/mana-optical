<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import { ShoppingCart, Heart, Search, SlidersHorizontal, X, Eye, ChevronDown, Tag } from 'lucide-vue-next'
import { apiFetch } from '../lib/api'

type ProductoApi = {
  id: number
  nombre: string
  slug: string
  descripcion: string
  precio: string
  precio_antes: string | null
  imagen_url: string
  categoria: { id: number; nombre: string; slug: string } | null
  marca: { id: number; nombre: string; slug: string } | null
}

type PaginatedResponse<T> = {
  count: number
  next: string | null
  previous: string | null
  results: T[]
}

type Producto = {
  id: number
  slug: string
  nombre: string
  categoria: string
  categoriaSlug: string
  marca: string
  precio: number
  precioAnterior: number | null
  oferta: boolean
  imagen: string
  descripcion: string
}

function formatPrecio(n: number): string {
  return `$${n.toLocaleString('es-CO')}`
}

function mapProducto(p: ProductoApi): Producto {
  const precio = Number(p.precio)
  const precioAnterior = p.precio_antes ? Number(p.precio_antes) : null
  return {
    id: p.id,
    slug: p.slug,
    nombre: p.nombre,
    categoria: p.categoria?.nombre ?? 'Sin categoría',
    categoriaSlug: p.categoria?.slug ?? '',
    marca: p.marca?.nombre ?? 'Sin marca',
    precio,
    precioAnterior,
    oferta: Boolean(precioAnterior && precioAnterior > precio),
    imagen: p.imagen_url || 'https://images.unsplash.com/photo-1574258495973-f010dfbb5371?auto=format&fit=crop&w=900&q=80',
    descripcion: p.descripcion || '',
  }
}

const productos = ref<Producto[]>([])
const cargando = ref(false)
const errorMsg = ref('')

const page = ref(1)
const hasNext = ref(false)
const cargandoMas = ref(false)

async function cargarProductos() {
  cargando.value = true
  errorMsg.value = ''
  page.value = 1
  hasNext.value = false

  try {
    const data = await apiFetch<PaginatedResponse<ProductoApi>>('/catalogo/productos/?page=1')
    productos.value = data.results.map(mapProducto)
    hasNext.value = Boolean(data.next)
  } catch (e) {
    productos.value = []
    errorMsg.value = e instanceof Error ? e.message : 'Error cargando productos'
  } finally {
    cargando.value = false
  }
}

async function cargarMas() {
  if (cargandoMas.value || !hasNext.value) return

  cargandoMas.value = true
  errorMsg.value = ''
  try {
    const nextPage = page.value + 1
    const data = await apiFetch<PaginatedResponse<ProductoApi>>(`/catalogo/productos/?page=${nextPage}`)
    productos.value = [...productos.value, ...data.results.map(mapProducto)]
    page.value = nextPage
    hasNext.value = Boolean(data.next)
  } catch (e) {
    errorMsg.value = e instanceof Error ? e.message : 'Error cargando más productos'
  } finally {
    cargandoMas.value = false
  }
}

const categoriaActiva = ref<string>('Todos')
const soloOfertas = ref(false)
const busqueda = ref('')
type OrdenOpc = 'relevancia' | 'precio-asc' | 'precio-desc' | 'nombre'
const ordenar = ref<OrdenOpc>('relevancia')
function setOrdenar(val: string) { ordenar.value = val as OrdenOpc }
const filtrosAbiertos = ref(false)
const quickView = ref<Producto | null>(null)
const wishlist = ref<Set<number>>(new Set())

const productosFiltrados = computed(() => {
  let lista = productos.value.filter((p: Producto) => {
    const catOk = categoriaActiva.value === 'Todos' || p.categoria === categoriaActiva.value
    const busOk = p.nombre.toLowerCase().includes(busqueda.value.toLowerCase())
    const ofertaOk = !soloOfertas.value || p.oferta
    return catOk && busOk && ofertaOk
  })
  if (ordenar.value === 'precio-asc') lista = [...lista].sort((a, b) => a.precio - b.precio)
  if (ordenar.value === 'precio-desc') lista = [...lista].sort((a, b) => b.precio - a.precio)
  if (ordenar.value === 'nombre') lista = [...lista].sort((a, b) => a.nombre.localeCompare(b.nombre))
  return lista
})

function toggleWishlist(id: number) {
  const s = new Set(wishlist.value)
  s.has(id) ? s.delete(id) : s.add(id)
  wishlist.value = s
}

function abrirQuickView(p: Producto) {
  quickView.value = p
  document.body.style.overflow = 'hidden'
}
function cerrarQuickView() {
  quickView.value = null
  document.body.style.overflow = ''
}

const opcionesOrden = [
  { value: 'relevancia', label: 'Relevancia' },
  { value: 'precio-asc', label: 'Menor precio' },
  { value: 'precio-desc', label: 'Mayor precio' },
  { value: 'nombre', label: 'Nombre A–Z' },
]

const categoriasList = computed(() => {
  const base = new Set<string>()
  for (const p of productos.value) base.add(p.categoria)
  return ['Todos', ...Array.from(base).sort((a, b) => a.localeCompare(b))]
})

onMounted(() => {
  cargarProductos()
})
</script>

<template>
  <div style="padding-top: var(--header-h, 4rem)">

    <!-- Hero -->
    <div class="bg-[#314037] py-14 px-6 text-center">
      <p class="text-[11px] tracking-[0.4em] uppercase text-[#f5d984] mb-3">Nuestra Tienda</p>
      <h1 class="text-3xl sm:text-4xl lg:text-5xl font-black text-white uppercase tracking-tight mb-3"
          style="font-family:'Playfair Display',serif;">
        Catálogo de Productos
      </h1>
      <p class="text-white/50 text-sm">Encuentra la montura perfecta para tu estilo de vida</p>
    </div>

    <!-- Layout: sidebar + grid -->
    <div class="max-w-screen-xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
      <div v-if="errorMsg" class="mb-6 border border-red-200 bg-red-50 px-4 py-3 text-[11px] text-red-700">
        {{ errorMsg }}
      </div>
      <div class="lg:flex lg:gap-10 lg:items-start">

        <!-- Sidebar (lg+) -->
        <aside class="hidden lg:block w-56 shrink-0 sticky top-[var(--header-h,4rem)] pt-1">

          <!-- Buscar -->
          <div class="relative mb-8">
            <Search class="absolute left-3 top-1/2 -translate-y-1/2 h-3.5 w-3.5 text-black/30" />
            <input
              v-model="busqueda" type="text" placeholder="Buscar..."
              class="w-full pl-9 pr-3 py-2.5 text-[11px] border border-black/15 outline-none focus:border-[#314037] transition"
            />
          </div>

          <!-- Categorías -->
          <div class="mb-8">
            <p class="text-[9px] font-black tracking-[0.28em] uppercase text-black/35 mb-3">Categoría</p>
            <div class="flex flex-col gap-1">
              <button
                v-for="cat in categoriasList" :key="cat"
                @click="categoriaActiva = cat"
                class="text-left px-3 py-2 text-[11px] font-semibold tracking-wide rounded transition-colors"
                :class="categoriaActiva === cat
                  ? 'bg-[#314037] text-[#f5d984]'
                  : 'text-black/60 hover:text-black hover:bg-black/5'"
              >{{ cat }}</button>
            </div>
          </div>

          <!-- Ordenar -->
          <div class="mb-8">
            <p class="text-[9px] font-black tracking-[0.28em] uppercase text-black/35 mb-3">Ordenar</p>
            <div class="flex flex-col gap-1">
              <button
                v-for="op in opcionesOrden" :key="op.value"
                @click="setOrdenar(op.value)"
                class="text-left px-3 py-2 text-[11px] font-semibold tracking-wide rounded transition-colors"
                :class="ordenar === op.value
                  ? 'text-[#314037] font-black'
                  : 'text-black/50 hover:text-black hover:bg-black/5'"
              >{{ op.label }}</button>
            </div>
          </div>

          <!-- Solo ofertas -->
          <label class="flex items-center gap-3 cursor-pointer group">
            <span
              class="h-4 w-4 border-2 flex items-center justify-center transition-colors shrink-0"
              :class="soloOfertas ? 'border-[#314037] bg-[#314037]' : 'border-black/25 group-hover:border-black/50'"
              @click="soloOfertas = !soloOfertas"
            >
              <span v-if="soloOfertas" class="block h-2 w-2 bg-[#f5d984]" />
            </span>
            <span class="text-[11px] font-semibold text-black/60 group-hover:text-black transition-colors">
              Solo ofertas
            </span>
          </label>
        </aside>

        <!-- Columna principal -->
        <div class="flex-1 min-w-0">

          <!-- Top bar móvil -->
          <div class="lg:hidden flex items-center justify-between mb-5 gap-3">
            <div class="relative flex-1 max-w-xs">
              <Search class="absolute left-3 top-1/2 -translate-y-1/2 h-3.5 w-3.5 text-black/30" />
              <input
                v-model="busqueda" type="text" placeholder="Buscar..."
                class="w-full pl-9 pr-3 py-2.5 text-[11px] border border-black/15 outline-none focus:border-[#314037] transition"
              />
            </div>
            <button
              @click="filtrosAbiertos = true"
              class="flex items-center gap-2 px-4 py-2.5 border border-black/15 text-[11px] font-bold tracking-wide uppercase hover:border-[#314037] transition shrink-0"
            >
              <SlidersHorizontal class="h-3.5 w-3.5" /> Filtros
            </button>
          </div>

          <!-- Top bar desktop -->
          <div class="hidden lg:flex items-center justify-between mb-8">
            <span class="text-[11px] text-black/40 font-medium">
              {{ productosFiltrados.length }}
              {{ productosFiltrados.length === 1 ? 'producto' : 'productos' }}
            </span>
            <div class="relative">
              <select
                v-model="ordenar"
                class="appearance-none pl-3 pr-8 py-2 text-[11px] font-semibold border border-black/15 outline-none focus:border-[#314037] cursor-pointer bg-white"
              >
                <option v-for="op in opcionesOrden" :key="op.value" :value="op.value">{{ op.label }}</option>
              </select>
              <ChevronDown class="absolute right-2.5 top-1/2 -translate-y-1/2 h-3.5 w-3.5 pointer-events-none text-black/40" />
            </div>
          </div>

          <!-- Grid de productos -->
          <div v-if="cargando" class="py-16 text-center text-[11px] text-black/40">
            Cargando productos...
          </div>
          <div class="grid grid-cols-2 md:grid-cols-3 xl:grid-cols-4 gap-x-4 gap-y-8 sm:gap-x-6 sm:gap-y-10">
            <div
              v-for="p in productosFiltrados"
              :key="p.id"
              class="group"
            >
              <!-- Imagen -->
              <div class="relative bg-[#f8f7f5] overflow-hidden mb-3 sm:mb-4">
                <RouterLink :to="`/producto/${p.slug}`" class="block">
                  <div class="h-44 sm:h-52 lg:h-56 flex items-center justify-center p-4 sm:p-6">
                    <img
                      :src="p.imagen" :alt="p.nombre"
                      class="h-full w-full object-contain transition-transform duration-700 group-hover:scale-105"
                    />
                  </div>
                </RouterLink>

                <!-- Badges -->
                <span v-if="p.oferta"
                  class="absolute top-2.5 left-2.5 sm:top-3 sm:left-3 bg-[#314037] text-[#f5d984] text-[9px] sm:text-[10px] font-bold tracking-widest uppercase px-2.5 py-1">
                  Oferta
                </span>

                <!-- Wishlist -->
                <button
                  @click="toggleWishlist(p.id)"
                  class="absolute top-2.5 right-2.5 sm:top-3 sm:right-3 h-7 w-7 sm:h-8 sm:w-8 flex items-center justify-center bg-white/90 backdrop-blur-sm shadow-sm transition hover:bg-white"
                  :aria-label="wishlist.has(p.id) ? 'Quitar de favoritos' : 'Agregar a favoritos'"
                >
                  <Heart
                    class="h-3.5 w-3.5 transition-colors"
                    :class="wishlist.has(p.id) ? 'fill-[#314037] text-[#314037]' : 'text-black/40'"
                  />
                </button>

                <!-- Acciones hover -->
                <div class="absolute inset-x-0 bottom-0 flex translate-y-full group-hover:translate-y-0 transition-transform duration-300">
                  <button
                    @click="abrirQuickView(p)"
                    class="flex-1 bg-white/95 text-black text-[10px] font-bold tracking-widest uppercase py-2.5 hover:bg-[#f5d984] transition-colors flex items-center justify-center gap-1.5 border-r border-black/8"
                  >
                    <Eye class="h-3.5 w-3.5" /> Ver rápido
                  </button>
                  <button class="flex-1 bg-[#314037] text-white text-[10px] font-bold tracking-widest uppercase py-2.5 hover:bg-[#f5d984] hover:text-[#314037] transition-colors flex items-center justify-center gap-1.5">
                    <ShoppingCart class="h-3.5 w-3.5" /> Carrito
                  </button>
                </div>
              </div>

              <!-- Info -->
              <div class="text-center px-1">
                <p class="text-[9px] sm:text-[10px] tracking-widest uppercase text-black/30 mb-1">{{ p.categoria }}</p>
                <RouterLink :to="`/producto/${p.slug}`" class="block">
                  <h3 class="text-[12px] sm:text-sm font-bold tracking-wide uppercase text-black hover:text-[#314037] transition-colors mb-2 leading-tight">
                    {{ p.nombre }}
                  </h3>
                </RouterLink>
                <div class="flex items-center justify-center gap-2">
                  <span v-if="p.precioAnterior" class="text-xs line-through text-black/25">{{ formatPrecio(p.precioAnterior) }}</span>
                  <span class="text-sm font-black text-[#314037]">{{ formatPrecio(p.precio) }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Estado vacío -->
          <div v-if="productosFiltrados.length === 0" class="text-center py-24 text-black/30">
            <Tag class="h-10 w-10 mx-auto mb-4 opacity-25" />
            <p class="text-sm font-semibold">No hay productos con ese criterio.</p>
            <button @click="categoriaActiva = 'Todos'; busqueda = ''; soloOfertas = false"
              class="mt-4 text-[11px] font-bold tracking-widest uppercase underline underline-offset-4 hover:text-black transition">
              Limpiar filtros
            </button>
          </div>

          <!-- Cargar más -->
          <div v-if="hasNext && productosFiltrados.length > 0" class="flex justify-center pt-12">
            <button
              :disabled="cargandoMas"
              @click="cargarMas"
              class="px-6 py-3 border border-black/15 text-[11px] font-black tracking-[0.28em] uppercase hover:border-[#314037] hover:text-[#314037] transition disabled:opacity-60"
            >
              {{ cargandoMas ? 'Cargando...' : 'Cargar más' }}
            </button>
          </div>
        </div>
      </div>
    </div>

  </div>

  <!-- Drawer de filtros (móvil) -->
  <transition name="fade">
    <div v-if="filtrosAbiertos" class="fixed inset-0 z-[85] lg:hidden">
      <div class="absolute inset-0 bg-black/40" @click="filtrosAbiertos = false" />
      <transition name="slide-left">
        <div class="absolute left-0 top-0 h-full w-72 max-w-[85vw] bg-white shadow-2xl flex flex-col overflow-y-auto">
          <div class="flex items-center justify-between border-b border-black/[0.08] px-5 py-4 shrink-0">
            <span class="text-[11px] font-black tracking-[0.28em] uppercase text-[#314037]">Filtros</span>
            <button @click="filtrosAbiertos = false" class="p-1.5 rounded-md text-black/50 hover:text-black hover:bg-black/5">
              <X class="h-5 w-5" />
            </button>
          </div>

          <div class="flex-1 px-5 py-5 space-y-7">
            <!-- Categorías -->
            <div>
              <p class="text-[9px] font-black tracking-[0.28em] uppercase text-black/35 mb-3">Categoría</p>
              <div class="flex flex-col gap-1">
                <button
                  v-for="cat in categoriasList" :key="cat"
                  @click="categoriaActiva = cat; filtrosAbiertos = false"
                  class="text-left px-3 py-2.5 text-[12px] font-semibold tracking-wide rounded transition-colors"
                  :class="categoriaActiva === cat ? 'bg-[#314037] text-[#f5d984]' : 'text-black/60 hover:bg-black/5'"
                >{{ cat }}</button>
              </div>
            </div>

            <!-- Ordenar -->
            <div>
              <p class="text-[9px] font-black tracking-[0.28em] uppercase text-black/35 mb-3">Ordenar por</p>
              <div class="flex flex-col gap-1">
                <button
                  v-for="op in opcionesOrden" :key="op.value"
                  @click="setOrdenar(op.value); filtrosAbiertos = false"
                  class="text-left px-3 py-2.5 text-[12px] font-semibold rounded transition-colors"
                  :class="ordenar === op.value ? 'text-[#314037] font-black' : 'text-black/50 hover:bg-black/5'"
                >{{ op.label }}</button>
              </div>
            </div>

            <!-- Solo ofertas -->
            <label class="flex items-center gap-3 cursor-pointer group px-1">
              <span
                class="h-5 w-5 border-2 flex items-center justify-center transition-colors shrink-0"
                :class="soloOfertas ? 'border-[#314037] bg-[#314037]' : 'border-black/25'"
                @click="soloOfertas = !soloOfertas"
              >
                <span v-if="soloOfertas" class="block h-2.5 w-2.5 bg-[#f5d984]" />
              </span>
              <span class="text-[12px] font-semibold text-black/60">Solo productos en oferta</span>
            </label>
          </div>
        </div>
      </transition>
    </div>
  </transition>

  <!-- Quick View modal -->
  <transition name="fade">
    <div v-if="quickView" class="fixed inset-0 z-[90] flex items-center justify-center p-4">
      <div class="absolute inset-0 bg-black/60 backdrop-blur-sm" @click="cerrarQuickView" />
      <transition name="scale-up">
        <div v-if="quickView" class="relative bg-white shadow-2xl w-full max-w-2xl max-h-[90vh] overflow-y-auto flex flex-col sm:flex-row">

          <!-- Botón cerrar -->
          <button @click="cerrarQuickView"
            class="absolute top-3 right-3 z-10 h-8 w-8 flex items-center justify-center bg-white shadow-md hover:bg-black/5 transition">
            <X class="h-4 w-4" />
          </button>

          <!-- Imagen -->
          <div class="sm:w-5/12 bg-[#f8f7f5] flex items-center justify-center p-8 min-h-[220px] sm:min-h-auto">
            <img :src="quickView.imagen" :alt="quickView.nombre"
              class="h-full w-full object-contain max-h-60 sm:max-h-80" />
          </div>

          <!-- Info -->
          <div class="sm:w-7/12 p-7 flex flex-col justify-between">
            <div>
              <div class="flex items-start justify-between gap-2 mb-1">
                <p class="text-[9px] tracking-widest uppercase text-black/35">{{ quickView.categoria }} · {{ quickView.marca }}</p>
                <span v-if="quickView.oferta"
                  class="shrink-0 bg-[#314037] text-[#f5d984] text-[9px] font-bold tracking-widest uppercase px-2 py-0.5">
                  Oferta
                </span>
              </div>
              <h2 class="text-xl sm:text-2xl font-black tracking-wide uppercase text-black mb-3"
                  style="font-family:'Playfair Display',serif;">
                {{ quickView.nombre }}
              </h2>
              <div class="flex items-center gap-3 mb-4">
                <span v-if="quickView.precioAnterior" class="text-sm line-through text-black/25">{{ formatPrecio(quickView.precioAnterior) }}</span>
                <span class="text-2xl font-black text-[#314037]">{{ formatPrecio(quickView.precio) }}</span>
              </div>
              <p class="text-sm text-black/55 leading-relaxed mb-6">{{ quickView.descripcion }}</p>
            </div>

            <!-- CTAs -->
            <div class="space-y-3">
              <button class="btn-shine w-full flex items-center justify-center gap-2 bg-[#314037] text-white text-[11px] font-bold tracking-[0.25em] uppercase py-3.5 hover:bg-[#f5d984] hover:text-[#314037] transition-colors duration-300">
                <ShoppingCart class="h-4 w-4" /> Añadir al carrito
              </button>
              <RouterLink
                :to="`/producto/${quickView.slug}`"
                @click="cerrarQuickView"
                class="w-full flex items-center justify-center gap-2 border border-black/20 text-[11px] font-bold tracking-[0.2em] uppercase py-3.5 hover:border-[#314037] hover:text-[#314037] transition-colors"
              >
                Ver ficha completa
              </RouterLink>
            </div>
          </div>
        </div>
      </transition>
    </div>
  </transition>
</template>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity .2s ease }
.fade-enter-from, .fade-leave-to { opacity: 0 }

.slide-left-enter-active, .slide-left-leave-active { transition: transform .25s cubic-bezier(0.4, 0, 0.2, 1) }
.slide-left-enter-from, .slide-left-leave-to { transform: translateX(-100%) }

.scale-up-enter-active, .scale-up-leave-active { transition: transform .2s ease, opacity .2s ease }
.scale-up-enter-from, .scale-up-leave-to { transform: scale(0.96); opacity: 0 }
</style>
