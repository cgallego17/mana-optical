<script setup lang="ts">
import { ref, computed } from 'vue'
import { ShoppingCart, Search, SlidersHorizontal } from 'lucide-vue-next'

const categorias = ['Todos', 'Monturas', 'Gafas de Sol', 'Lentes de Contacto', 'Accesorios']
const categoriaActiva = ref('Todos')
const busqueda = ref('')

const productos = [
  { id: 1, nombre: 'Lennons Metálicos', categoria: 'Monturas', precio: 175000, precioAnterior: 199000, oferta: true, imagen: 'https://images.unsplash.com/photo-1574258495973-f010dfbb5371?auto=format&fit=crop&w=600&q=80' },
  { id: 2, nombre: 'Gafas Cat Eye', categoria: 'Monturas', precio: 199000, precioAnterior: null, oferta: false, imagen: 'https://images.unsplash.com/photo-1508296695146-257a814070b4?auto=format&fit=crop&w=600&q=80' },
  { id: 3, nombre: 'Aviador Clásico', categoria: 'Gafas de Sol', precio: 211000, precioAnterior: null, oferta: false, imagen: 'https://images.unsplash.com/photo-1572635196237-14b3f281503f?auto=format&fit=crop&w=600&q=80' },
  { id: 4, nombre: 'Ovaladas Carey', categoria: 'Gafas de Sol', precio: 189000, precioAnterior: 220000, oferta: true, imagen: 'https://images.unsplash.com/photo-1582142306909-195724d33ffc?auto=format&fit=crop&w=600&q=80' },
  { id: 5, nombre: 'Montura Delgada', categoria: 'Monturas', precio: 165000, precioAnterior: null, oferta: false, imagen: 'https://images.unsplash.com/photo-1509695507497-903c140c43b0?auto=format&fit=crop&w=600&q=80' },
  { id: 6, nombre: 'Redondas Clip-On', categoria: 'Monturas', precio: 225000, precioAnterior: null, oferta: false, imagen: 'https://images.unsplash.com/photo-1473496169904-658ba7574b0d?auto=format&fit=crop&w=600&q=80' },
  { id: 7, nombre: 'Sol Cuadradas', categoria: 'Gafas de Sol', precio: 195000, precioAnterior: null, oferta: false, imagen: 'https://images.unsplash.com/photo-1577803645773-f96470509666?auto=format&fit=crop&w=600&q=80' },
  { id: 8, nombre: 'Estuche Premium', categoria: 'Accesorios', precio: 35000, precioAnterior: null, oferta: false, imagen: 'https://images.unsplash.com/photo-1574258495973-f010dfbb5371?auto=format&fit=crop&w=600&q=80' },
  { id: 9, nombre: 'Paño Microfibra', categoria: 'Accesorios', precio: 15000, precioAnterior: null, oferta: false, imagen: 'https://images.unsplash.com/photo-1508296695146-257a814070b4?auto=format&fit=crop&w=600&q=80' },
]

const productosFiltrados = computed(() => {
  return productos.filter(p => {
    const categoriaOk = categoriaActiva.value === 'Todos' || p.categoria === categoriaActiva.value
    const busquedaOk = p.nombre.toLowerCase().includes(busqueda.value.toLowerCase())
    return categoriaOk && busquedaOk
  })
})

const formatPrecio = (n: number) => `$${n.toLocaleString('es-CO')}`
</script>

<template>
  <div class="pt-[108px]">

    <!-- Hero tienda -->
    <div class="bg-[#314037] py-16 px-8 text-center">
      <p class="text-[11px] tracking-[0.4em] uppercase text-[#f5d984] mb-3">Nuestra Tienda</p>
      <h1 class="text-4xl lg:text-5xl font-black text-white uppercase tracking-tight mb-3" style="font-family:'Playfair Display',serif;">
        Catálogo de Productos
      </h1>
      <p class="text-white/50 text-sm">Encuentra la montura perfecta para tu estilo de vida</p>
    </div>

    <div class="w-full bg-white py-16 px-8 lg:px-16">

      <!-- Filtros -->
      <div class="flex flex-col sm:flex-row gap-4 mb-12 max-w-6xl mx-auto">
        <!-- Búsqueda -->
        <div class="relative flex-1">
          <Search class="absolute left-4 top-1/2 -translate-y-1/2 h-4 w-4 text-black/30" />
          <input
            v-model="busqueda"
            type="text"
            placeholder="Buscar producto..."
            class="w-full pl-11 pr-4 py-3 border border-black/15 text-sm outline-none focus:border-[#314037] transition"
          />
        </div>
        <!-- Categorías -->
        <div class="flex gap-2 flex-wrap">
          <button
            v-for="cat in categorias"
            :key="cat"
            @click="categoriaActiva = cat"
            class="px-5 py-3 text-[11px] font-bold tracking-widest uppercase transition-all duration-300"
            :class="categoriaActiva === cat
              ? 'bg-[#314037] text-[#f5d984]'
              : 'border border-black/15 text-black/60 hover:border-[#314037] hover:text-[#314037]'"
          >
            {{ cat }}
          </button>
        </div>
      </div>

      <!-- Grid de productos -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-x-6 gap-y-12 max-w-6xl mx-auto">
        <div
          v-for="producto in productosFiltrados"
          :key="producto.id"
          class="group cursor-pointer"
        >
          <div class="relative bg-[#f8f7f5] overflow-hidden mb-4">
            <div class="h-52 flex items-center justify-center p-6">
              <img :src="producto.imagen" :alt="producto.nombre"
                class="h-full w-full object-contain transition-transform duration-700 group-hover:scale-105" />
            </div>
            <span v-if="producto.oferta"
              class="absolute top-3 left-3 bg-[#314037] text-[#f5d984] text-[10px] font-bold tracking-widest uppercase px-3 py-1">
              Oferta
            </span>
            <div class="absolute inset-x-0 bottom-0 translate-y-full group-hover:translate-y-0 transition-transform duration-300">
              <button class="btn-shine w-full bg-[#314037] text-white text-[11px] font-bold tracking-widest uppercase py-3 hover:bg-[#f5d984] hover:text-[#314037] transition-colors duration-300 flex items-center justify-center gap-2">
                <ShoppingCart class="h-3.5 w-3.5" /> Añadir al carrito
              </button>
            </div>
          </div>
          <div class="text-center">
            <p class="text-[10px] tracking-widest uppercase text-black/35 mb-1">{{ producto.categoria }}</p>
            <h3 class="text-sm font-bold tracking-wide uppercase text-black mb-2">{{ producto.nombre }}</h3>
            <div class="flex items-center justify-center gap-2">
              <span v-if="producto.precioAnterior" class="text-xs line-through text-black/25">{{ formatPrecio(producto.precioAnterior) }}</span>
              <span class="text-sm font-black text-[#314037]">{{ formatPrecio(producto.precio) }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Sin resultados -->
      <div v-if="productosFiltrados.length === 0" class="text-center py-20 text-black/35">
        <SlidersHorizontal class="h-10 w-10 mx-auto mb-4 opacity-30" />
        <p class="text-sm">No se encontraron productos con ese criterio.</p>
      </div>

    </div>
  </div>
</template>
