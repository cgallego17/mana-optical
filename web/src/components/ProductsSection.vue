<script setup lang="ts">
import { ref, onMounted } from 'vue'

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
}

type PaginatedResponse<T> = {
  count: number
  next: string | null
  previous: string | null
  results: T[]
}

type ProductCard = {
  id: number
  name: string
  category: string
  price: number
  originalPrice: number | null
  sale: boolean
  image: string
  slug: string
}

const products = ref<ProductCard[]>([])
const cargando = ref(false)

function mapProduct(p: ProductoApi): ProductCard {
  const price = Number(p.precio)
  const originalPrice = p.precio_antes ? Number(p.precio_antes) : null
  return {
    id: p.id,
    name: p.nombre,
    category: p.categoria?.nombre ?? 'Sin categoría',
    price,
    originalPrice,
    sale: Boolean(originalPrice && originalPrice > price),
    image: p.imagen_url || 'https://images.unsplash.com/photo-1574258495973-f010dfbb5371?auto=format&fit=crop&w=700&q=80',
    slug: p.slug,
  }
}

async function cargar() {
  cargando.value = true
  try {
    const data = await apiFetch<PaginatedResponse<ProductoApi>>('/catalogo/productos/?page=1&page_size=6')
    products.value = data.results.map(mapProduct)
  } catch {
    products.value = []
  } finally {
    cargando.value = false
  }
}

onMounted(() => {
  cargar()
})
</script>

<template>
  <section class="w-full bg-white py-24 px-8 lg:px-16">

    <!-- Header -->
    <div v-scroll-reveal class="flex flex-col items-center text-center mb-20">
      <span class="inline-block text-[11px] tracking-[0.35em] uppercase text-[#f5d984] mb-4 font-medium">Colección 2025</span>
      <h2 class="text-4xl lg:text-5xl font-black tracking-tight text-black uppercase mb-5">Nuestros Productos</h2>
      <p class="text-sm text-black/40 leading-relaxed">Explora nuestra selección de monturas de diseño exclusivo para cada estilo</p>
    </div>

    <!-- Grid -->
    <div v-if="cargando" class="py-10 text-center text-[11px] text-black/40">
      Cargando...
    </div>
    <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-x-8 gap-y-14 max-w-6xl mx-auto">
      <div
        v-for="(product, i) in products"
        :key="product.id"
        v-scroll-reveal="{ delay: (i % 3) * 150 }"
        class="group cursor-pointer"
      >
        <!-- Image area -->
        <div class="relative bg-[#f8f7f5] overflow-hidden mb-5">
          <div class="h-60 flex items-center justify-center p-6">
            <img
              :src="product.image"
              :alt="product.name"
              class="h-full w-full object-contain transition-transform duration-700 group-hover:scale-108"
            />
          </div>

          <!-- Sale badge -->
          <span v-if="product.sale"
            class="absolute top-4 left-4 bg-[#314037] text-white text-[10px] font-bold tracking-[0.2em] uppercase px-3 py-1.5">
            Oferta
          </span>

          <!-- Add to cart — slide up on hover -->
          <div class="absolute inset-x-0 bottom-0 translate-y-full group-hover:translate-y-0 transition-transform duration-400 ease-out">
            <button class="btn-shine active:scale-95 w-full bg-[#314037] text-white text-[11px] font-bold tracking-[0.25em] uppercase py-4
              hover:bg-[#f5d984] hover:text-[#314037] transition-colors duration-300">
              + Añadir al carrito
            </button>
          </div>
        </div>

        <!-- Info -->
        <div class="text-center px-2">
          <p class="text-[10px] tracking-[0.3em] uppercase text-black/35 mb-2">{{ product.category }}</p>
          <h3 class="text-sm font-bold tracking-wide uppercase text-black mb-3">{{ product.name }}</h3>
          <div class="flex items-center justify-center gap-3">
            <span v-if="product.originalPrice" class="text-sm line-through text-black/25">
              ${{ product.originalPrice.toLocaleString('es-CO') }}
            </span>
            <span class="text-base font-black text-black">${{ product.price.toLocaleString('es-CO') }}</span>
          </div>
        </div>
      </div>
    </div>

  </section>
</template>
