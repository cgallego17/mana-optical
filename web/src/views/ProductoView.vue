<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useRoute, RouterLink } from 'vue-router'
import { ShoppingCart, Heart, ChevronLeft, ChevronRight, MessageCircle, Tag, ArrowLeft } from 'lucide-vue-next'
import { useAgendaModal } from '../composables/agendaModal'
import { apiFetch } from '../lib/api'

const route = useRoute()
const { open: openAgenda } = useAgendaModal()

type ProductoDetailApi = {
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

type ProductoListApi = {
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

type ProductoVm = {
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
  imagenes: string[]
  descripcion: string
  disponible: boolean
}

function formatPrecio(n: number): string {
  return `$${n.toLocaleString('es-CO')}`
}

function mapProductoDetail(p: ProductoDetailApi): ProductoVm {
  const precio = Number(p.precio)
  const precioAnterior = p.precio_antes ? Number(p.precio_antes) : null
  const imagen = p.imagen_url || 'https://images.unsplash.com/photo-1574258495973-f010dfbb5371?auto=format&fit=crop&w=900&q=80'
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
    imagen,
    imagenes: [imagen],
    descripcion: p.descripcion || '',
    disponible: true,
  }
}

function mapProductoList(p: ProductoListApi): ProductoVm {
  return mapProductoDetail(p)
}

const producto = ref<ProductoVm | null>(null)
const relacionados = ref<ProductoVm[]>([])
const cargando = ref(false)
const errorMsg = ref('')

async function cargarProducto(slug: string) {
  cargando.value = true
  errorMsg.value = ''
  producto.value = null
  relacionados.value = []

  try {
    const data = await apiFetch<ProductoDetailApi>(`/catalogo/productos/${slug}/`)
    producto.value = mapProductoDetail(data)

    if (producto.value.categoriaSlug) {
      const rel = await apiFetch<ProductoListApi[]>(
        `/catalogo/productos/?categoria=${encodeURIComponent(producto.value.categoriaSlug)}`,
      )
      relacionados.value = rel
        .map(mapProductoList)
        .filter(p => p.id !== producto.value?.id)
        .slice(0, 4)
    }
  } catch (e) {
    errorMsg.value = e instanceof Error ? e.message : 'Error cargando producto'
  } finally {
    cargando.value = false
  }
}

const imagenActiva = ref(0)
const cantidad = ref(1)
const enWishlist = ref(false)

watch(
  () => route.params.slug,
  (val) => {
    if (typeof val === 'string' && val) cargarProducto(val)
  },
)

onMounted(() => {
  const slug = route.params.slug
  if (typeof slug === 'string' && slug) cargarProducto(slug)
})

function waLink(nombre: string) {
  const msg = encodeURIComponent(`Hola, me interesa el producto *${nombre}*. ¿Podrían darme más información?`)
  return `https://wa.me/573005262309?text=${msg}`
}
</script>

<template>
  <div style="padding-top: var(--header-h, 4rem)">

    <div v-if="errorMsg" class="px-6 pt-6">
      <div class="border border-red-200 bg-red-50 px-4 py-3 text-[11px] text-red-700">
        {{ errorMsg }}
      </div>
    </div>

    <div v-if="cargando" class="min-h-[60vh] flex items-center justify-center text-center px-6">
      <p class="text-[11px] text-black/40">Cargando producto...</p>
    </div>

    <!-- Producto no encontrado -->
    <div v-if="!producto" class="min-h-[60vh] flex flex-col items-center justify-center text-center px-6">
      <Tag class="h-12 w-12 text-black/20 mb-4" />
      <h2 class="text-xl font-bold mb-2">Producto no encontrado</h2>
      <p class="text-sm text-black/45 mb-6">El producto que buscas no existe o fue eliminado.</p>
      <RouterLink to="/tienda"
        class="inline-flex items-center gap-2 text-[11px] font-bold tracking-widest uppercase border border-black/20 px-6 py-3 hover:border-[#314037] hover:text-[#314037] transition">
        <ArrowLeft class="h-3.5 w-3.5" /> Volver a la tienda
      </RouterLink>
    </div>

    <template v-else>

      <!-- Breadcrumb -->
      <div class="border-b border-black/[0.06] bg-[#f8f7f5]">
        <div class="max-w-screen-xl mx-auto px-4 sm:px-6 lg:px-8 py-3 flex items-center gap-2 text-[11px] text-black/40">
          <RouterLink to="/" class="hover:text-black transition">Inicio</RouterLink>
          <span>/</span>
          <RouterLink to="/tienda" class="hover:text-black transition">Tienda</RouterLink>
          <span>/</span>
          <span class="text-black/70 font-semibold">{{ producto.nombre }}</span>
        </div>
      </div>

      <!-- Detalle principal -->
      <section class="max-w-screen-xl mx-auto px-4 sm:px-6 lg:px-8 py-10 lg:py-16">
        <div class="lg:grid lg:grid-cols-2 lg:gap-16 xl:gap-24">

          <!-- Galería de imágenes -->
          <div class="mb-8 lg:mb-0">
            <div class="relative bg-[#f8f7f5] overflow-hidden">
              <div class="h-64 sm:h-80 lg:h-[480px] flex items-center justify-center p-8">
                <img
                  :src="producto.imagenes[imagenActiva]"
                  :alt="producto.nombre"
                  class="h-full w-full object-contain transition-opacity duration-300"
                />
              </div>

              <!-- Flechas galería -->
              <template v-if="producto.imagenes.length > 1">
                <button
                  @click="imagenActiva = (imagenActiva - 1 + producto.imagenes.length) % producto.imagenes.length"
                  class="absolute left-3 top-1/2 -translate-y-1/2 h-9 w-9 flex items-center justify-center bg-white/90 shadow hover:bg-white transition">
                  <ChevronLeft class="h-4 w-4" />
                </button>
                <button
                  @click="imagenActiva = (imagenActiva + 1) % producto.imagenes.length"
                  class="absolute right-3 top-1/2 -translate-y-1/2 h-9 w-9 flex items-center justify-center bg-white/90 shadow hover:bg-white transition">
                  <ChevronRight class="h-4 w-4" />
                </button>
              </template>
            </div>

            <!-- Miniaturas -->
            <div v-if="producto.imagenes.length > 1" class="flex gap-2 mt-3">
              <button
                v-for="(img, i) in producto.imagenes" :key="i"
                @click="imagenActiva = i"
                class="h-16 w-16 bg-[#f8f7f5] flex items-center justify-center p-2 border-2 transition"
                :class="imagenActiva === i ? 'border-[#314037]' : 'border-transparent hover:border-black/20'"
              >
                <img :src="img" :alt="`Vista ${i+1}`" class="h-full w-full object-contain" />
              </button>
            </div>
          </div>

          <!-- Info del producto -->
          <div class="flex flex-col">

            <!-- Categoría + oferta -->
            <div class="flex items-center gap-3 mb-2">
              <span class="text-[10px] tracking-[0.3em] uppercase text-black/35">{{ producto.categoria }}</span>
              <span v-if="producto.oferta"
                class="bg-[#314037] text-[#f5d984] text-[9px] font-bold tracking-widest uppercase px-2.5 py-0.5">
                Oferta
              </span>
            </div>

            <!-- Nombre -->
            <h1 class="text-3xl sm:text-4xl font-black tracking-wide uppercase text-black mb-1 leading-tight"
                style="font-family:'Playfair Display',serif;">
              {{ producto.nombre }}
            </h1>
            <p class="text-[11px] text-black/35 tracking-widest uppercase mb-5">{{ producto.marca }}</p>

            <!-- Precio -->
            <div class="flex items-end gap-3 mb-6 pb-6 border-b border-black/[0.08]">
              <span class="text-3xl font-black text-[#314037]">{{ formatPrecio(producto.precio) }}</span>
              <span v-if="producto.precioAnterior" class="text-base line-through text-black/25 mb-1">
                {{ formatPrecio(producto.precioAnterior) }}
              </span>
              <span v-if="producto.precioAnterior" class="text-[10px] font-bold text-[#314037] bg-[#f5d984]/30 px-2 py-0.5 mb-1">
                -{{ Math.round((1 - producto.precio / producto.precioAnterior) * 100) }}%
              </span>
            </div>

            <!-- Descripción -->
            <p class="text-sm text-black/55 leading-relaxed mb-8">{{ producto.descripcion }}</p>

            <!-- Cantidad -->
            <div class="flex items-center gap-4 mb-6">
              <span class="text-[10px] font-black tracking-[0.2em] uppercase text-black/40">Cantidad</span>
              <div class="flex items-center border border-black/15">
                <button
                  @click="cantidad = Math.max(1, cantidad - 1)"
                  class="h-9 w-9 flex items-center justify-center text-black/50 hover:text-black hover:bg-black/5 transition text-lg font-bold">
                  −
                </button>
                <span class="w-10 text-center text-sm font-bold">{{ cantidad }}</span>
                <button
                  @click="cantidad++"
                  class="h-9 w-9 flex items-center justify-center text-black/50 hover:text-black hover:bg-black/5 transition text-lg font-bold">
                  +
                </button>
              </div>
            </div>

            <!-- CTAs -->
            <div class="flex flex-col sm:flex-row gap-3 mb-5">
              <button class="btn-shine flex-1 flex items-center justify-center gap-2 bg-[#314037] text-white text-[11px] font-bold tracking-[0.25em] uppercase py-4 hover:bg-[#f5d984] hover:text-[#314037] transition-colors duration-300">
                <ShoppingCart class="h-4 w-4" /> Añadir al carrito
              </button>
              <button
                @click="enWishlist = !enWishlist"
                class="sm:w-14 flex items-center justify-center border border-black/15 py-4 hover:border-[#314037] transition"
                :aria-label="enWishlist ? 'Quitar de favoritos' : 'Agregar a favoritos'"
              >
                <Heart class="h-4 w-4 transition-colors" :class="enWishlist ? 'fill-[#314037] text-[#314037]' : 'text-black/40'" />
              </button>
            </div>
            <a
              :href="waLink(producto.nombre)"
              target="_blank"
              class="w-full flex items-center justify-center gap-2 border border-black/20 text-[11px] font-bold tracking-[0.2em] uppercase py-3.5 hover:border-[#314037] hover:text-[#314037] transition-colors"
            >
              <MessageCircle class="h-4 w-4" /> Consultar por WhatsApp
            </a>

            <!-- Detalles adicionales -->
            <div class="mt-8 pt-6 border-t border-black/[0.08] space-y-2 text-[11px] text-black/45">
              <div class="flex items-center gap-2">
                <span class="font-bold text-black/60">Marca:</span> {{ producto.marca }}
              </div>
              <div class="flex items-center gap-2">
                <span class="font-bold text-black/60">Disponibilidad:</span>
                <span :class="producto.disponible ? 'text-green-600' : 'text-red-500'">
                  {{ producto.disponible ? 'En stock' : 'Agotado' }}
                </span>
              </div>
            </div>
          </div>

        </div>
      </section>

      <!-- Productos relacionados -->
      <section v-if="relacionados.length" class="bg-[#f8f7f5] py-16 px-4 sm:px-6 lg:px-8">
        <div class="max-w-screen-xl mx-auto">
          <div class="mb-8 text-center">
            <p class="text-[10px] tracking-[0.35em] uppercase text-[#314037] font-semibold mb-2">También te puede gustar</p>
            <h2 class="text-2xl font-black uppercase tracking-tight">Productos relacionados</h2>
          </div>
          <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4 sm:gap-6">
            <div v-for="rel in relacionados" :key="rel.id" class="group">
              <RouterLink :to="`/producto/${rel.slug}`" class="block bg-white overflow-hidden mb-3">
                <div class="h-40 sm:h-48 flex items-center justify-center p-5">
                  <img :src="rel.imagen" :alt="rel.nombre"
                    class="h-full w-full object-contain transition-transform duration-500 group-hover:scale-105" />
                </div>
              </RouterLink>
              <RouterLink :to="`/producto/${rel.slug}`" class="block text-center">
                <p class="text-[9px] tracking-widest uppercase text-black/30 mb-1">{{ rel.categoria }}</p>
                <h3 class="text-xs font-bold tracking-wide uppercase text-black hover:text-[#314037] transition-colors mb-1.5">
                  {{ rel.nombre }}
                </h3>
                <span class="text-sm font-black text-[#314037]">{{ formatPrecio(rel.precio) }}</span>
              </RouterLink>
            </div>
          </div>
        </div>
      </section>

      <!-- CTA Agenda -->
      <section class="bg-[#314037] py-14 px-6 text-center">
        <p class="text-white/60 text-sm mb-2">¿Necesitas asesoría o examen visual?</p>
        <h3 class="text-xl font-black text-white uppercase mb-6" style="font-family:'Playfair Display',serif;">
          Agenda tu cita con nuestros especialistas
        </h3>
        <button
          @click="openAgenda()"
          class="btn-shine inline-flex items-center gap-3 bg-[#f5d984] text-[#314037] text-[11px] font-bold tracking-[0.25em] uppercase px-10 py-4 hover:opacity-90 transition-opacity"
        >
          Reservar Cita
        </button>
      </section>

    </template>
  </div>
</template>
